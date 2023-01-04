# AntiPlagiarism
Проверка на плагиат кода, разработанная на языке программирования Python
Данный алгоритм основан на расстоянии Левенштейна
Его отличительной особенностью является тот факт, что он может определять, что некоторые import-ы, функции и методы поменялись местами, по сравнению с оригинальным файлом. Но это стоило асимптотики работы. Вместо O(n^2) у оригинального алгоритма поиска расстояния Левенштейна, асимптотика данного алгоритма составляет O(n^4)
