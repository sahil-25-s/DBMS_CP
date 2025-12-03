import simple_sqlite as db

try:
    print("Testing get_show_by_id function...")
    result = db.get_show_by_id(1)
    print("Result:", result)
    print("Result length:", len(result) if result else "None")
    
    if result:
        for i, val in enumerate(result):
            print(f"Index {i}: {val}")
            
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()