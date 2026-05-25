from app.bots.bot_admin.db.connection import get_connection

# =====================
# DATABASE
# =====================

# conn = get_connection()
# cursor = conn.cursor()

# =====================



def insert_booking(datetime_start, datetime_end, type, price, event_id, name, comment):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO bookings (start_time, end_time, type, price, event_id, name, comment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (datetime_start, datetime_end, type, price, event_id, name, comment)
        )
        conn.commit()
        print(f"Booking inserted successfully: {name} from {datetime_start} to {datetime_end}")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_event_id(booking_datetime):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT event_id FROM bookings WHERE start_time = %s",
            (booking_datetime,)
        )
        conn.commit()
        result = cursor.fetchone()
        
        if result:
            print(f"Event_id successfully extracted: {result}")
            return result[0] # Возвращаем event_id
        else:
            print("Booking not found")
            return None
        
    except Exception as e:
        print(f"Error occurred while extracting event_id: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()



def delete_booking_from_bd(event_id):
    
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM bookings WHERE event_id = %s",
            (event_id,)
        )

        conn.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def update_booking(event_id, datetime_start, datetime_end, type, price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE bookings SET datetime_start = %s, datetime_end = %s, type = %s, price = %s WHERE event_id = %s",
            (datetime_start, datetime_end, type, price, event_id)
        )
        conn.commit()
        print(f"Booking updated successfully: {event_id}")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def set_keybox_codes(code):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO keybox_codes (code) VALUES (%s)",
                (code,)
            )
        conn.commit()
        print(f"Keybox code inserted successfully: {code}")
        return code

    except Exception as e:
        conn.rollback()
        print(f"Error occurred in set_keybox_codes: {e}")
        raise

    finally:
        conn.close()

def get_last_keybox_code():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT code 
            FROM keybox_codes
            ORDER BY id DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
    except Exception as e:
        print(f"Error occurred in: {e}")
        result = None
    finally:
        cursor.close()
        conn.close()
    return result[0] if result else None
