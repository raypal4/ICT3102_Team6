import pymongo
from datasource.Database import Database
import time
class StaffGateway:
    # Static
    __StaffCollection = Database.db["staff"]

    # Get all staff locations withint the 15 min period
    def retrieve_all_staff(self):
        collection = StaffGateway.__StaffCollection
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 900 #15 min record
        all_staff = collection.find({"timestamp": {"$gte": start_timestamp, "$lte": end_timestamp }}, {"_id":0}).sort("timestamp", -1)
        return list(all_staff)

    # retrieve all locations detected within the timestamp for one user
    def retrieve_staff_location(self, id, start_time, end_time):
        collection = StaffGateway.__StaffCollection
        allStaffVisitedLocations = collection.find({"staff_id": id}).sort("timestamp", -1)
        temp = []
        for item in allStaffVisitedLocations:
            # if timestamp is greater then the endtime, break out of the loop. Dont need to check the rest
            if int(item["timestamp"]) > end_time:
                break
            if start_time <= int(item["timestamp"]) <= end_time:
                item.pop('_id', None)
                item.pop('rssi', None)
                item.pop('mac', None)
                item.pop('staff_id', None)
                temp.append(item)
        return temp

    # add new location based on user and detected beacon to the db
    def add_new_staff_location(self, user_address, level, location, rssi, beacon_address):
        new_location = {
            "level": level,
            "location": location,
            "timestamp": int(time.time()),
            "rssi": rssi,
            "mac": beacon_address,
            "staff_id": user_address
        }
        collection = StaffGateway.__StaffCollection
        try:
            collection.insert_one(
                new_location
            )
            return True
        except Exception as e:
            print(e)
