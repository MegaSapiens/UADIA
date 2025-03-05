class UniversalAgent:
    def __init__(self):
        self.name = "Универсальный Агент УАДИА"
        self.knowledge_base = {}
        self.skills = []

    def learn(self, new_knowledge):
        """Добавляет новую информацию в базу знаний"""
        self.knowledge_base.update(new_knowledge)

    def acquire_skill(self, skill):
        """Добавляет новый навык агенту"""
        if skill not in self.skills:
            self.skills.append(skill)
            print(f"Навык {skill} добавлен.")

    def process_task(self, task):
        """Обрабатывает задачу с использованием имеющихся навыков и знаний"""
        for skill in self.skills:
            if skill in task:
                return f"Используя навык {skill}, я могу обработать эту задачу."
        
        relevant_info = [info for info in self.knowledge_base.values() if any(task.lower() info.lower())]
        if relevant_info:
            return f"На основе моих знаний: {relevant_info[0]}"
        
        return "Я не знаю, как справиться с этой задачей."

    def get_status(self):
        """Возвращает текущее состояние агента"""
        return {
            "name": self.name,
            "skills": self.skills,
            "knowledge_base_size": len(self.knowledge_base),
            "last_learned": max(self.knowledge_base.keys(), key=lambda x: x if isinstance(x, str) else 0, default="Никогда")
        }

# Пример использования
universal_agent = UniversalAgent()
universal_agent.learn({"Python": "Программный язык", "Java": "Операционная система"})
universal_agent.acquire_skill("Y4:0")
print(universal_agent.process_task("Какой это язык программирования?"))
print(universal_agent.get_status())

'''
Этот код создает класс UniversalAgent, который представляет собой универсального агента УАДИА. Основные функции:

- learn: Добавляет новые знания в базу данных.
- acquire_skill: Добавляет новый навык  списку доступных.
- process_task: Обрабатывает задачу, используя имеющиеся навыки и знания.
- get_status: Возвращает текущее состояние агента.

Класс реализует основные принципы УАДИА, позволяя ему учиться, приобретать новые навыки и обрабатывать различные задачи на основе
 имеющихся знаний и возможностей.
'''
