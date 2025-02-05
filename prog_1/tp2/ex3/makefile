# Définir les variables pour les fichiers source et objets
CXX = g++                 # Le compilateur à utiliser
CXXFLAGS = -std=c++20 # Les options de compilation (pour activer les avertissements et spécifier la norme C++11)
OBJECTS = main.o class_dynamic_vector.o # Les fichiers objets à compiler
TARGET = main               # Le nom de l'exécutable

# Règle par défaut : compilation et exécution
all: $(TARGET)
	./$(TARGET)


# Règle pour compiler l'exécutable à partir des fichiers objets
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

# Règle pour compiler main.o à partir de main.cpp
main.o: main.cpp class_dynamic_vector.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp

# Règle pour compiler class_point.o à partir de class_point.cpp
class_dynamic_vector.o: class_dynamic_vector.cpp class_dynamic_vector.hpp
	$(CXX) $(CXXFLAGS) -c class_dynamic_vector.cpp

# Règle pour nettoyer les fichiers objets et l'exécutable
clean:
	rm -f $(OBJECTS) $(TARGET)
