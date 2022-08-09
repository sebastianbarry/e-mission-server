import emission.core.get_database as edb
import emission.core.wrapper.user as ewu

for ue in edb.get_uuid_db().find():
    trip_count = edb.get_analysis_timeseries_db().count_documents({"user_id": ue["uuid"], "metadata.key": "analysis/confirmed_trip"})
    location_count = edb.get_timeseries_db().count_documents({"user_id": ue["uuid"], "metadata.key": "background/location"})
    last_trip = list(edb.get_analysis_timeseries_db().find({"user_id": ue["uuid"], "metadata.key": "analysis/confirmed_trip"}).sort("data.end_ts", -1).limit(1))
    last_trip_time = last_trip[0]["data"]["end_fmt_time"] if len(last_trip) > 0 else None
    print(f"For {ue['user_email']}: Trip count = {trip_count}, location count = {location_count}, last trip = {last_trip_time}")
    confirmed_pct, valid_replacement_pct, score = ewu.User.computeConfirmed(ue)
    print(f"for the last month: Confirmed label percentage = %{confirmed_pct}, Valid replacement label percentage = %{valid_replacement_pct}, Label score = %{score}")