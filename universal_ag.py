class UniversalAgent:
    def __init__(self):
        self.name = "Универсальный Агент УАДИА"
        self.knowledge_base = []

    def learn(self, new_knowledge: dict) -> None:
        """Добавляет новую информацию в базу знаний"""
        for key, value in new_knowledge.items():
            self.knowledge_base.append(("knowledge", key, value))

    def acquire_skill(self, skill: str) -> None:
        """Добавляет новый навык агенту"""
        if not any(triplet for triplet in self.knowledge_base if triplet == ("skill", skill, None)):
            self.knowledge_base.append(("skill", skill, None))
            print(f"Навык {skill} добавлен.")

    def process_task(self, task: str) -> str:
        """Обрабатывает задачу с использованием имеющихся навыков и знаний"""
        for triplet in self.knowledge_base:
            if triplet[0] == "skill" and triplet[1] in task:
                return f"Используя навык {triplet[1]}, я могу обработать эту задачу."
        
        relevant_info = [triplet[2] for triplet in self.knowledge_base if triplet[0] == "knowledge" and task.lower() in triplet[2].lower()]
        if relevant_info:
            return f"На основе моих знаний: {relevant_info[0]}"
        
        return "Я не знаю, как справиться с этой задачей."

    def get_status(self) -> dict:
        """Возвращает текущее состояние агента"""
        skills = [triplet[1] for triplet in self.knowledge_base if triplet[0] == "skill"]
        knowledge_count = len([triplet for triplet in self.knowledge_base if triplet[0] == "knowledge"])
        last_learned = max((triplet[1] for triplet in self.knowledge_base if triplet[0] == "knowledge"), key=lambda x: x if isinstance(x, str) else 0, default="Никогда")
        
        return {
            "name": self.name,
            "skills": skills,
            "knowledge_base_size": knowledge_count,
            "last_learned": last_learned
        }

# Пример использования
if __name__ == "__main__":
    universal_agent = UniversalAgent()
    universal_agent.learn({"Python": "Программный язык", "Java": "Операционная система"})
    universal_agent.acquire_skill("Y4:0")
    print(universal_agent.process_task("Какой это язык программирования?"))
    print(universal_agent.get_status())
