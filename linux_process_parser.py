from datetime import datetime
import subprocess
from collections import defaultdict


def get_system_info():
    users = set()
    process_counts = defaultdict(int)
    total_processes = 0
    total_memory_used = 0
    total_cpu_usage = 0
    top_memory_process = None
    max_memory = 0
    top_cpu_process = None
    max_cpu = 0

    all_processes_info = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
    for line in all_processes_info.stdout.splitlines()[1:]:
        sys_processes = line.split()
        user_name = sys_processes[0]
        memory_used = sys_processes[3]
        cpu_usage = sys_processes[2]
        command = ' '.join(sys_processes[10:])[:20]

        users.add(user_name)
        process_counts[user_name] += 1
        total_processes += 1

        try:
            memory_used = float(memory_used[:-1])
            total_memory_used += memory_used
            if memory_used > max_memory:
                max_memory = memory_used
                top_memory_process = command
        except ValueError:
            pass

        try:
            cpu_usage = float(cpu_usage)
            total_cpu_usage += cpu_usage
            if cpu_usage > max_cpu:
                max_cpu = cpu_usage
                top_cpu_process = command
        except ValueError:
            pass

    report = f"Отчёт о состоянии системы:\n"
    report += f"Пользователи системы: {', '.join(users)}\n"
    report += f"Процессов запущено: {total_processes}\n\n"

    report += f"Пользовательских процессов:\n"
    for user_name, count in process_counts.items():
        report += f"{user_name}: {count}\n"
    report += "\n"

    report += f"Всего памяти используется: {total_memory_used / total_processes:.1f}%\n"
    report += f"Всего CPU используется: {total_cpu_usage / total_processes:.1f}%\n"
    report += f"Больше всего памяти использует: {top_memory_process} ({max_memory:.1f}%)\n"
    report += f"Больше всего CPU использует: {top_cpu_process} ({max_cpu:.1f}%)\n"

    print(report)

    return report


def save_report(report):
    datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{datetime_str}-scan.txt"
    with open(filename, 'w') as file:
        file.write(report)


if __name__ == '__main__':
    system_report = get_system_info()
    save_report(system_report)
