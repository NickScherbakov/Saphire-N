def view_latest_test_results():
    with get_db_connection() as conn:
        # Последние тесты
        latest_tests = conn.execute('''
            SELECT DISTINCT test_name, timestamp 
            FROM model_dialogues 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''').fetchall()
        
        for test in latest_tests:
            print(f"\n=== Тест: {test['test_name']} ===")
            print(f"Время: {test['timestamp']}")
            
            # Сообщения в тесте
            messages = conn.execute('''
                SELECT model_name, message_type, message_content, aspect
                FROM model_dialogues
                WHERE test_name = ?
                ORDER BY sequence_number
            ''', (test['test_name'],)).fetchall()
            
            for msg in messages:
                print(f"\nМодель: {msg['model_name']}")
                if msg['aspect']:
                    print(f"Аспект: {msg['aspect']}")
                print(f"Тип: {msg['message_type']}")
                print(f"Сообщение: {msg['message_content']}")
                print("-" * 40)

# Вызов функции для просмотра результатов
view_latest_test_results()