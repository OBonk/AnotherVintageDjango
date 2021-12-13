from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from AnotherVintage.views import dbconn
from bson.objectid import ObjectId

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    print("Caught")
    if ipn.payment_status == 'Completed':
        # payment was successful
        db = dbconn()
        oid = ObjectId(ipn.invoice)
        order = db["orders"].find_one({"_id":oid})
        cost = db["stock"].find_one({"_id":order["stockID"]})["price"]
        if cost == ipn.mc_gross:
            # mark the order as paid
            db["orders"].update_one({"_id":oid},{ "$set": { "status": "sold" } })
            db["stock"].update_one({"_id":order["stockID"]}, { "$set": { "status": "sold" } })