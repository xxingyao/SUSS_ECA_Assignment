from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash

from models.forms import BookForm

from models.users import User
from models.package import Package
from models.book import Booking

from datetime import date, timedelta, datetime

booking = Blueprint('bookingController', __name__) # use bookingController.fn

@booking.route('/view')
@login_required
def view():
    form = BookForm()
    hotel_name=request.args.get('hotel_name').strip("'")

    the_package_to_be_booked = Package.getPackage(hotel_name=hotel_name)
    print(the_package_to_be_booked)
    return render_template('booking.html', panel=hotel_name, form=form, package=the_package_to_be_booked)

@booking.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        hotel_name=request.form.get("hotel_name")
        check_in_date=request.form.get("check_in_date") 
        # print('check_in_date in book', check_in_date, type(check_in_date))
        # check_in_date in book 2023-03-28 <class 'str'>

        existing_package = Package.getPackage(hotel_name=hotel_name)
        print(existing_package)
        if (current_user is None) or (existing_package is None):
            print(f"Something is wrong")
        else:
            aBooking = Booking.createBooking(check_in_date, current_user, existing_package) 
            # print('aBooking.check_in_date', aBooking.check_in_date, type(aBooking.check_in_date)) # type is str
            # aBooking.check_in_date 2023-03-28 <class 'str'>
        return redirect(url_for('packageController.packages'))

@booking.route('/manageBooking')
@login_required
def manageBooking(days = -2000):
    status = request.args.get('status')
    bookings = list(Booking.getUserBookingsFromDate(customer=current_user, from_date=date.today()+timedelta(days = days), status=None if status == "" else status))
    if bookings:
        bookings.sort(key = lambda b: b.check_in_date)
    return render_template('userBookings.html', panel='Manage Booking', bookings=bookings, selected_status = status)

@booking.route("/updateBooking", methods=["POST"])
@login_required
def update():
    hotel_name=request.form.get("hotel_name")
    old_check_in_date=request.form.get("old_check_in_date")
    new_check_in_date=request.form.get("check_in_date")
    status=request.form.get("status")
    
    Booking.updateBooking(old_check_in_date, new_check_in_date, current_user, hotel_name, status)
    flash("Booking has been updated", "info")
    return redirect(url_for('bookingController.manageBooking'))
     
@booking.route("/deleteBooking", methods=["POST"])
@login_required
def delete():
    hotel_name=request.form.get("hotel_name")
    check_in_date=request.form.get("old_check_in_date")
    status=request.form.get("status")

    # print(check_in_date, type(check_in_date))
    # convert check_in_date to date type ?? check
    # 2023-03-09 00:00:00 <class 'str'>
    Booking.deleteBooking(check_in_date, current_user, hotel_name, status)
    flash("Booking has been deleted", "info")

    return redirect(url_for('bookingController.manageBooking'))

@booking.route("/cancelBooking", methods=["POST"])
@login_required
def cancel():
    try:
        hotel_name=request.form.get("hotel_name")
        check_in_date=request.form.get("old_check_in_date")
        status=request.form.get("status")
        Booking.cancelBooking(check_in_date, current_user, hotel_name, status)
        flash("Booking has been cancelled", "info")
    except ValueError as e:
        flash("Error cancelling booking", "info")

    return redirect(url_for('bookingController.manageBooking'))   