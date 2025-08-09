from models.users import User
from models.package import Package
from app import db
from mongoengine.queryset.visitor import Q
from datetime import datetime
from collections import defaultdict


class Booking(db.Document):

    meta = {'collection': 'booking'}
    check_in_date = db.DateTimeField(required=True)
    customer = db.ReferenceField(User)
    package = db.ReferenceField(Package)
    total_cost = db.FloatField()
    status = db.StringField()

    def calculate_total_cost(self):
        self.total_cost = self.package.duration * self.package.unit_cost
        self.save()

    @staticmethod
    def getBookingsGroupedByUserAndStatus():
        all_bookings = Booking.objects()
        user_booking_counts = defaultdict(
            lambda: {'cancelled': 0, 'completed': 0, 'upcoming': 0})

        for booking in all_bookings:
            user_email = booking.customer.email
            status = booking.status

            if status == 'cancelled':
                user_booking_counts[user_email]['cancelled'] += 1
            elif status == 'completed':
                user_booking_counts[user_email]['completed'] += 1
            elif status == 'upcoming':
                user_booking_counts[user_email]['upcoming'] += 1

        return user_booking_counts

    @staticmethod
    def getBookingsByEmail(email, status=None):
        customer = User.getUser(email)
        if customer:
            query = Q(customer=customer)
            if status:
                query &= Q(status=status)
            return Booking.objects(query)
        return []

    @staticmethod
    def getAllBookings(status=None):
        query = Q()
        if status:
            query &= Q(status=status)
        return Booking.objects(query)

    @staticmethod
    def createBooking(check_in_date, customer, package, status=None):
        today = datetime.now()

        if isinstance(check_in_date, str):
            check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
        elif isinstance(check_in_date, datetime):
            check_in_date_obj = check_in_date
        
        if status is None:
            if check_in_date_obj <= today:
                status = 'completed'
            else:
                status = 'upcoming'

        booking = Booking(check_in_date=check_in_date,
                          customer=customer, package=package, status=status).save()
        booking.calculate_total_cost()
        return booking

    @staticmethod
    def getUserBookingsFromDate(customer, from_date, status=None):
        query = Q(customer=customer) & Q(check_in_date__gte=from_date)
        if status:
            query &= Q(status=status)
        return Booking.objects(query)

    @staticmethod
    def getBooking(check_in_date, customer, hotel_name, status=None):
        package = Package.getPackage(hotel_name)
        return Booking.objects(Q(customer=customer) & Q(check_in_date=check_in_date) & Q(package=package) & Q(status=status)).first()

    @staticmethod
    def updateBooking(old_check_in_date, new_check_in_date, customer, hotel_name, status=None):
        booking = Booking.getBooking(
            old_check_in_date, customer, hotel_name, status)
        new_check_in_date_obj = datetime.strptime(
            new_check_in_date, "%Y-%m-%d").date()
        today = datetime.today().date()  # Get today's date

        if booking:
            booking.check_in_date = new_check_in_date
            if new_check_in_date_obj <= today:
                booking.status = "completed"
            return booking.save()

    @staticmethod
    def deleteBooking(check_in_date, customer, hotel_name, status=None):
        booking = Booking.getBooking(
            check_in_date, customer, hotel_name, status)
        if booking:
            booking.delete()
        return booking

    @staticmethod
    def cancelBooking(check_in_date, customer, hotel_name, status=None):
        booking = Booking.getBooking(
            check_in_date, customer, hotel_name, status)
        if booking:
            booking.status = "cancelled"
            return booking.save()
