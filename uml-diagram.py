# Добавление легенды к диаграмме UML
uml.node('Legend', '''Legend:
- OpenAIAssistant: Главный компонент, обрабатывающий запросы пользователя.
- DatabaseManager: Менеджер для хранения данных (запросов и результатов).
- AgentInterface: Базовый интерфейс для всех агентов.
- OllamaAgent: Агент, реализующий анализ данных.
- GigaChatAgent: Агент, генерирующий отчёты и визуализации.''', shape='note')

# Связь легенды с диаграммой (условная)
uml.edge('Legend', 'OpenAIAssistant', style='dotted', arrowhead='none')

# Перегенерация диаграммы с легендой
uml.render('/mnt/data/Saphire-N_UML_with_Legend', view=False)
'/mnt/data/Saphire-N_UML_with_Legend.png'
