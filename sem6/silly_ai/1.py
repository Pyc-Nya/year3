import time
from collections import deque
from dataclasses import dataclass
from typing import Optional, List, Tuple, Set


# Вариант 4: начальное (г), целевое (Г), стратегии: в глубину, двунаправленный
# 0 обозначает пустой участок
INITIAL_STATE = (
    (6, 0, 8),
    (5, 2, 1),
    (4, 3, 7)
)


GOAL_STATE = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)


# Словарь смещений для действий Left/Right/Up/Down
MOVES = {'Left': (0, -1), 'Right': (0, 1), 'Up': (-1, 0), 'Down': (1, 0)}
# Обратное действие для двунаправленного поиска (путь от цели к старту → от старта к цели) для двунаправленного поиска
REVERSE_MOVE = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}



    
# Узел дерева поиска: State, Parent, Action, Path-Cost, Depth
@dataclass
class Node:
    state: Tuple[Tuple[int, ...], ...] # состояние доски
    parent: Optional['Node'] = None # ссылка на родителя
    action: Optional[str] = None # действие, которым пришли в это состояние
    path_cost: int = 0 # g(n)
    depth: int = 0 # глубина в дереве
    # Хеширование состояния для хранения в множестве visited
    def __hash__(self):
        return hash(self.state)
    # Проверка на равенство состояний
    def __eq__(self, other):
        if other is None:
            return False
        return self.state == other.state




# Приводит состояние к хешируемому кортежу для хранения в множестве visited.
def state_to_tuple(state) -> tuple:
    return tuple(tuple(row) for row in state)




# ищет пустую клетку (0) в состоянии
def find_blank(state) -> Tuple[int, int]:
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1




# Проверяет, что координата (row, col) лежит в пределах доски 3×3.
def is_valid_move(row: int, col: int) -> bool:
    return 0 <= row < 3 and 0 <= col < 3




# Применяет ход (Left/Right/Up/Down) к состоянию, двигая пустую клетку; возвращает новое состояние или None.
def apply_move(state, blank_row: int, blank_col: int, move: str) -> Optional[tuple]:
    dr, dc = MOVES[move]
    new_row, new_col = blank_row + dr, blank_col + dc
    if not is_valid_move(new_row, new_col):
        return None


    state_list = [list(row) for row in state]
    state_list[blank_row][blank_col], state_list[new_row][new_col] = \
        state_list[new_row][new_col], state_list[blank_row][blank_col]
    return tuple(tuple(row) for row in state_list)




# Функция последователей: допустимые переходы (действие, новое_состояние).
def get_successors(state) -> List[Tuple[str, tuple]]:
    r, c = find_blank(state)
    out = []
    for action in MOVES:
        new_state = apply_move(state, r, c, action)
        if new_state is not None: # если ход возможен, добавляем его в список
            out.append((action, new_state)) # действие и новое состояние
    return out




# Проверяет, совпадает ли состояние с целевым.
def is_goal(state) -> bool:
    return state == GOAL_STATE # проверяем, совпадает ли состояние с целевым




# Выводит состояние доски в консоль (пустая клетка — пробел).
def print_state(state):
    for row in state:
        print(' '.join(str(c) if c else ' ' for c in row)) # выводим состояние доски в консоль
    print()




# Восстанавливает путь от узла до корня (список узлов).
def path_to_root(node: Node) -> List[Node]:
    path = []
    while node:
        path.append(node)
        node = node.parent
    return list(reversed(path))


 
def _actions_from_path(path: List[Node], reverse_backward: bool = False) -> List[str]:
    """Список ходов по пути. Если reverse_backward — развернуть и заменить на обратные (для обратного дерева)."""
    nodes = reversed(path[1:]) if reverse_backward else path
    if reverse_backward: # если reverse_backward, то разворачиваем и заменяем на обратные
        return [REVERSE_MOVE[n.action] for n in nodes if n.action]
    return [n.action for n in nodes if n.action]


 # выводит решение и статистику при встрече двух направлений
def _print_bidir_solution(forward_node: Node, backward_node: Node, stats: 'SearchStats', elapsed: float):
    """Печать решения и статистики при встрече двух направлений."""
    actions = _actions_from_path(path_to_root(forward_node)) + _actions_from_path(path_to_root(backward_node), reverse_backward=True)
    print(">>> ЦЕЛЕВОЕ СОСТОЯНИЕ ДОСТИГНУТО (встреча направлений)! <<<")
    print(f"\nРешение найдено за {len(actions)} ходов:")
    for i, action in enumerate(actions, 1):
        print(f"  Ход {i}: {action}")
    _print_complexity_stats("Двунаправленный поиск", stats, elapsed)




# Выводит экспериментальные оценки: время выполнения, количество итераций, количество узлов.
def _print_complexity_stats(algorithm: str, stats: 'SearchStats', elapsed_sec: float):
    print(f"\n--- Экспериментальная оценка сложности ({algorithm}) ---")
    print(f"Время выполнения: {elapsed_sec:.4f} сек")
    print(f"Количество итераций: {stats.steps}")
    print(f"Количество узлов: {stats.nodes_generated}")
    print(f"Ёмкостная сложность (макс. размер каймы, ед. памяти): {stats.max_frontier_size}")




# Статистика для оценки сложности
class SearchStats:
    def __init__(self):
        self.steps = 0          # количество шагов (итераций)
        self.nodes_expanded = 0  # раскрытых вершин
        self.nodes_generated = 0 # сгенерированных узлов
        self.max_frontier_size = 0 # максимальный размер каймы
        self.duplicates_found = 0 # количество повторных состояний




# Поиск в глубину (DFS): кайма как стек (LIFO), раскрывается последняя добавленная вершина.
def depth_first_search(step_mode: bool = True):
    stats = SearchStats() # инициализируем статистику
    frontier = deque([Node(INITIAL_STATE)]) # кайма как стек (LIFO), раскрывается последняя добавленная вершина.
    visited: Set[tuple] = {state_to_tuple(INITIAL_STATE)} # множество посещенных состояний
    stats.nodes_generated = 1 # количество сгенерированных узлов


    print("=" * 50)
    print("ПОИСК В ГЛУБИНУ")
    print("=" * 50)
    print("Начальное состояние:")
    print_state(INITIAL_STATE)


    t0 = time.perf_counter() # время начала поиска
    while frontier: # пока кайма не пуста
        stats.steps += 1 # количество шагов
        stats.max_frontier_size = max(stats.max_frontier_size, len(frontier)) # максимальный размер каймы


        # Выбираем вершину с конца (LIFO - стек)
        node = frontier.pop()
        stats.nodes_expanded += 1 # количество раскрытых вершин


        if step_mode: # если режим пошаговый, выводим информацию о шаге
            print(f"\n--- Шаг {stats.steps} ---")
            print(f"Раскрываемая вершина (глубина={node.depth}):")
            print_state(node.state)


        # если достигнуто целевое состояние, выводим решение и статистику
        if is_goal(node.state):
            elapsed = time.perf_counter() - t0 # время окончания поиска
            print(">>> ЦЕЛЕВОЕ СОСТОЯНИЕ ДОСТИГНУТО! <<<")
            path = path_to_root(node) # путь от корня до текущей вершины
            print(f"\nРешение найдено за {len(path) - 1} ходов:")
            for i, n in enumerate(path): # выводим путь
                if n.action:
                    print(f"  Ход {i}: {n.action}")
                print_state(n.state) # выводим состояние доски
            _print_complexity_stats("Поиск в глубину", stats, elapsed) # выводим статистику
            return node, stats


        successors = get_successors(node.state) # получаем последователей
        new_nodes = []


        for action, new_state in successors: # для каждого последователя
            state_t = state_to_tuple(new_state) # преобразуем состояние в хешируемый кортеж
            if state_t in visited: # если состояние уже посещено, пропускаем
                stats.duplicates_found += 1 # количество повторных состояний
                if step_mode:
                    print(f"  Повторное состояние (пропуск): действие {action}")
                continue


            visited.add(state_t) # добавляем состояние в множество посещенных
            child = Node(new_state, node, action, node.path_cost + 1, node.depth + 1) # создаем нового узла
            frontier.append(child) # добавляем в кайму
            new_nodes.append((action, child)) # добавляем в список новых узлов
            stats.nodes_generated += 1 # количество сгенерированных узлов


        if step_mode:
            if new_nodes:
                print("Добавленные вершины:")
                for action, child in new_nodes:
                    print(f"  {action}: глубина={child.depth}")
                    print_state(child.state)
            print(f"Текущая кайма: {len(frontier)} вершин")
            input("Нажмите Enter для следующего шага...")


    elapsed = time.perf_counter() - t0
    print("Решение не найдено (пространство поиска может быть бесконечным для DFS)") # если решение не найдено, выводим сообщение
    _print_complexity_stats("Поиск в глубину", stats, elapsed)
    return None, stats




# Двунаправленный поиск: BFS от начального и от целевого состояния, встреча в середине.
# Предшественники в 8-ка совпадают с последователями (ходы обратимы).
def bidirectional_search(step_mode: bool = True):
    stats = SearchStats()
    # Прямое направление: от начального состояния
    frontier_forward = deque([Node(INITIAL_STATE)])
    visited_forward: Set[tuple] = {state_to_tuple(INITIAL_STATE)}
    forward_node_by_state: dict = {state_to_tuple(INITIAL_STATE): frontier_forward[0]}
    # Обратное направление: от целевого состояния
    frontier_backward = deque([Node(GOAL_STATE)])
    visited_backward: Set[tuple] = {state_to_tuple(GOAL_STATE)}
    backward_node_by_state: dict = {state_to_tuple(GOAL_STATE): frontier_backward[0]}
    stats.nodes_generated = 2


    print("=" * 50)
    print("ДВУНАПРАВЛЕННЫЙ ПОИСК (BFS от старта и от цели)")
    print("=" * 50)
    print("Начальное состояние:")
    print_state(INITIAL_STATE)
    print("Целевое состояние:")
    print_state(GOAL_STATE)


    t0 = time.perf_counter()
    while frontier_forward and frontier_backward: # пока каймы не пусты
        stats.steps += 1 # количество шагов
        stats.max_frontier_size = max(
            stats.max_frontier_size, # максимальный размер каймы
            len(frontier_forward) + len(frontier_backward) # сумма размеров кайм
        )


        # Раскрываем одну вершину в прямом направлении
        node_f = frontier_forward.popleft() # извлекаем вершину из каймы вперёд
        stats.nodes_expanded += 1 # количество раскрытых вершин


        if step_mode: # если режим пошаговый, выводим информацию о шаге
            print(f"\n--- Шаг {stats.steps} (прямое направление) ---")
            print("Раскрываемая вершина:")
            print_state(node_f.state)


        if state_to_tuple(node_f.state) in visited_backward: # если состояние уже посещено в обратном направлении, выводим решение и статистику
            _print_bidir_solution(node_f, backward_node_by_state[state_to_tuple(node_f.state)], stats, time.perf_counter() - t0)
            return node_f, stats
       # для каждого последователя
        for action, new_state in get_successors(node_f.state):
            state_t = state_to_tuple(new_state)
            if state_t in visited_forward: # если состояние уже посещено в прямом направлении, пропускаем
                stats.duplicates_found += 1
                if step_mode:
                    print(f"  Повторное состояние (пропуск): действие {action}")
                continue
            visited_forward.add(state_t)
            child = Node(new_state, node_f, action, node_f.path_cost + 1, node_f.depth + 1)
            forward_node_by_state[state_t] = child
            frontier_forward.append(child) # добавляем в кайму вперёд
            stats.nodes_generated += 1 # количество сгенерированных узлов
            if step_mode:
                print(f"  Добавлена вершина: {action}")
            if state_t in visited_backward: # если состояние уже посещено в обратном направлении, выводим решение и статистику
                _print_bidir_solution(child, backward_node_by_state[state_t], stats, time.perf_counter() - t0)
                return child, stats


        if step_mode:
            print(f"Кайма (вперёд): {len(frontier_forward)} вершин")
            input("Нажмите Enter для следующего шага...")


        # Раскрываем одну вершину в обратном направлении
        node_b = frontier_backward.popleft()
        stats.nodes_expanded += 1 # количество раскрытых вершин


        if step_mode:
            print(f"\n--- Шаг {stats.steps + 1} (обратное направление) ---")
            print("Раскрываемая вершина (от цели):")
            print_state(node_b.state)
 
        if state_to_tuple(node_b.state) in visited_forward: # если состояние уже посещено в прямом направлении, выводим решение и статистику
            _print_bidir_solution(forward_node_by_state[state_to_tuple(node_b.state)], node_b, stats, time.perf_counter() - t0)
            return forward_node_by_state[state_to_tuple(node_b.state)], stats
        # для каждого последователя
        for action, new_state in get_successors(node_b.state):
            state_t = state_to_tuple(new_state)
            if state_t in visited_backward: # если состояние уже посещено в обратном направлении, пропускаем
                stats.duplicates_found += 1
                if step_mode:
                    print(f"  Повторное состояние (пропуск): действие {action}")
                continue
            visited_backward.add(state_t)
            child_b = Node(new_state, node_b, action, node_b.path_cost + 1, node_b.depth + 1)
            backward_node_by_state[state_t] = child_b
            frontier_backward.append(child_b)
            stats.nodes_generated += 1
           
            if step_mode:
                print(f"  Добавлена вершина (от цели): {action}")
            if state_t in visited_forward:
                _print_bidir_solution(forward_node_by_state[state_t], child_b, stats, time.perf_counter() - t0)
                return forward_node_by_state[state_t], stats
        if step_mode:
            print(f"Кайма (назад): {len(frontier_backward)} вершин")
            input("Нажмите Enter для следующего шага...")


    elapsed = time.perf_counter() - t0
    print("Решение не найдено")
    _print_complexity_stats("Двунаправленный поиск", stats, elapsed)
    return None, stats




def main():
    print("Выберите режим:")
    print("1 - Пошаговый (каждый шаг по Enter)")
    print("2 - Автоматический (без пауз)")
    mode = input("Ваш выбор (1/2): ").strip() or "1"
    step_mode = mode == "1"


    print("\nВыберите стратегию (вариант 4):")
    print("1 - Поиск в глубину")
    print("2 - Двунаправленный поиск")
    choice = input("Ваш выбор (1/2): ").strip()


    if choice == "1":
        depth_first_search(step_mode)
    elif choice == "2":
        bidirectional_search(step_mode)
    else:
        print("Неверный выбор")




if __name__ == "__main__":
    main()