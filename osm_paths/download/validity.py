def bbox_validity_check(bbox_str):
    try:
        bbox = tuple(float(coord) for coord in bbox_str.split(","))
        if len(bbox) != 4:
            raise Exception(
                "Bounding box coordinates have 4 coordinates seperated by ',': minlon,minlat,maxlon,maxlat"
            )

        minlon, minlat, maxlon, maxlat = bbox

        # latitude range
        if not (-90.0 <= minlat <= 90.0) or not (-90.0 <= maxlat <= 90.0):
            raise Exception(
                "latitude coordinate out of range: it must be between -90 and 90"
            )

        # longitude range
        if not -180.0 <= minlon <= 180.0 or not -180.0 <= maxlon <= 180.0:
            raise Exception(
                "longitude coordinate out of range: it must be between -180 and 180"
            )

        # latitude order
        if maxlat <= minlat:
            raise Exception("latitude coordinates are in the incorrect order")

        # longitude order
        if maxlon <= minlon:
            raise Exception("longitude coordinates are in the incorrect order")

        return minlon, minlat, maxlon, maxlat

    except Exception:
        raise
