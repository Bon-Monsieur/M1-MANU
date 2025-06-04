# Nom de l'exécutable C++
EXEC = main
SRC = main.cpp
OBJ = $(SRC:.cpp=.o)

# Compilateur
CXX = g++
CXXFLAGS = -Wall -std=c++20

# Script Python
PY_SCRIPT = tracer_solution.py

# Compilation C++
all: $(EXEC)

$(EXEC): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Nettoyage
clean:
	rm -f $(OBJ) $(EXEC)

fclean: clean

re: fclean all

# Exécution du binaire C++
run_cpp: $(EXEC)
	./$(EXEC)

# Exécution du script Python
run_py:
	python $(PY_SCRIPT)

# Exécuter les deux
run_all: run_cpp run_py

.PHONY: all clean fclean re run_cpp run_py run_all
