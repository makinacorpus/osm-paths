def bbox_validity_check(bbox_str, CustomError):
    try:
        bbox = tuple(float(coord) for coord in bbox_str.split(','))
        if len(bbox) != 4:
            raise CustomError()
    except CustomError:
        raise CustomError("Bounding box coordinates have 4 coordinates seperated by ',': minlon,minlat,maxlon,maxlat")

    minlon, minlat, maxlon, maxlat = bbox

    # latitude range
    if not -90.0 <= minlat <= 90.0 or not -90.0 <= maxlat <= 90.0:
        raise CustomError('latitude coordinate out of range: it must be between -90 and 90')

    # longitude range
    if not -180.0 <= minlon <= 180.0 or not -180.0 <= maxlon <= 180.0:
        raise CustomError('longitude coordinate out of range: it must be between -180 and 180')

    # latitude order
    if maxlat <= minlat:
        raise CustomError('latitude coordinates are in the incorrect order')

    # longitude order
    if maxlon <= minlon:
        raise CustomError('longitude coordinates are in the incorrect order')

    return minlon, minlat, maxlon, maxlat
