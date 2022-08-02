from decimal import Decimal
from django.conf import settings
from gari.models import Vehicle


class Compare(object):
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(settings.COMPARE_SESSION_ID)
        if not compare:
            compare = self.session[settings.COMPARE_SESSION_ID] = {}
        self.compare = compare

    def add(self, vehicle):
        vehicle_id = str(vehicle.id)
        if vehicle_id not in self.compare:
            self.compare[vehicle_id] = {'price': str(vehicle.price)}
            self.session.modified = True


    def save(self):
        self.compare[settings.COMPARE_SESSION_ID] = self.compare
        self.session.modified = True

    def remove(self, vehicle):
        vehicle_id = str(vehicle.id)
        if vehicle_id in self.compare:
            del self.compare[vehicle_id]
            self.session.modified = True




    def __iter__(self):
        vehicle_ids = self.compare.keys()
        vehicles = Vehicle.objects.filter(id__in=vehicle_ids)
        for vehicle in vehicles:
            self.compare[str(vehicle.id)]['vehicle'] = vehicle
        for item in self.compare.values():
            yield item



    def clear(self):
        del self.session[settings.COMPARE_SESSION_ID]
        self.session.modified = True




