import pymongo
import logging


def create_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.addHandler(logging.NullHandler())
    return logger

def mongo_safe_write(records, collection, _continue_on_error=True, update=False):
    logger = create_logger(__name__)
    if not records:
        return
    if not update:
        try:
            collection.insert(records, continue_on_error=_continue_on_error)
        except pymongo.errors.DuplicateKeyError as e:
                pass
        except Exception, e:
            logger.error("Mongodb insertion failed")
            raise e
    else:
        for record in records:
            try:
                collection.insert(record, continue_on_error=_continue_on_error)
            except pymongo.errors.DuplicateKeyError as e:
                collection.update({"_id": record["_id"]}, record)
                pass
            except Exception, e:
                logger.error(record)
                raise e
