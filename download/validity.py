def bbox_validity_check(bbox, CustomError):
    minlat, minlon, maxlat, maxlon = bbox

    # latitude range
    if not -90.0 <= minlat <= 90.0 or not -90.0 <= maxlat <= 90.0:
        print(minlat, maxlat)
        raise CustomError('latitude coordinate out of range: it must be between -90 and 90')

    # longitude range
    if not -180.0 <= minlon <= 180.0 or not -180.0 <= maxlon <= 180.0:
        print(minlon, maxlon)
        raise CustomError('longitude coordinate out of range: it must be between -180 and 180')

    # latitude order
    if maxlat <= minlat:
        raise CustomError('latitude coordinates are in the incorrect order')

    # longitude order
    if maxlon <= minlon:
        raise CustomError('longitude coordinates are in the incorrect order')