#include <iostream>
#include <vector>
#include <cctype>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <map>
#include <sstream>
using namespace std;

// Funciones ahorcado
// Función para elegir una palabra random del vector de palabras
string elegir_palabra(const vector<string>& palabras_lista ) {
    srand(time(nullptr));
    return palabras_lista [rand() % palabras_lista .size()];
    
}

// Función para poner guiones bajos

string guion_(const string& palabra) {
    string adivinar = palabra; 
    for(int i = 0; i < adivinar.length(); i++) { 
        if (adivinar[i] != ' ') { 
            adivinar[i] = '_'; 
        }
    }
    return adivinar;
}


//  Funcion que chequea si la letra ingresada es correcto
void letra_correcta(const string& palabra, string& adivinar, char letra) {
    for (int i = 0; i < palabra.length(); ++i) {
        if (palabra[i] == letra) {
            adivinar[i] = letra;
        }
    }
}

// Juego en si

void ahorcado(){
    vector<string> palabras_lista = {"computacion","expo","toriggia", "lenguaje", "programacion", "computadora", "calippo","windows","linux","rojas","scanio","estudio","politecnico","lealtad"};
    string palabra = elegir_palabra(palabras_lista);
    string adivinar = guion_(palabra);

    const int maximo_de_intentos = 7;
    int intentos = 0;
    char letra;

    cout << "Bienvenido al juego del ahorcado!" << endl;

    while (intentos < maximo_de_intentos && adivinar != palabra) {
        cout << "Palabra a adivinar: " << adivinar << endl;
        cout << "Intentos restantes: " << maximo_de_intentos - intentos << endl;
        cout << "Ingresa una letra: ";
        cin >> letra;
        if (palabra.find(letra) != -1) { // el -1 indica que la letra no se encontro en la palabra
                cout << "¡Correcto!" << endl;
            letra_correcta(palabra, adivinar, letra);
        } else {
            cout << "Incorrecto. Intenta de nuevo." << endl;
            intentos++;
        }
    }

    if (adivinar == palabra) {
cout<< endl;
        cout << " ██████╗  █████╗ ███╗   ██╗ █████╗ ███████╗████████╗███████╗██╗██╗"<< endl;
        cout << "██╔════╝ ██╔══██╗████╗  ██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║██║"<< endl;
        cout << "██║  ███╗███████║██╔██╗ ██║███████║███████╗   ██║   █████╗  ██║██║"<< endl;
        cout << "██║   ██║██╔══██║██║╚██╗██║██╔══██║╚════██║   ██║   ██╔══╝  ╚═╝╚═╝"<< endl;
        cout << "╚██████╔╝██║  ██║██║ ╚████║██║  ██║███████║   ██║   ███████╗██╗██╗"<< endl;
        cout << " ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝"<< endl;

        cout<< "Has adivinado la palabra: " << palabra << endl;    } 
        else {
            cout <<endl;
            cout << "██████╗ ███████╗██████╗ ██████╗ ██╗███████╗████████╗███████╗██╗██╗" << endl;
            cout << "██╔══██╗██╔════╝██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝██╔════╝██║██║" << endl;
            cout << "██████╔╝█████╗  ██████╔╝██║  ██║██║███████╗   ██║   █████╗  ██║██║" << endl;
            cout << "██╔═══╝ ██╔══╝  ██╔══██╗██║  ██║██║╚════██║   ██║   ██╔══╝  ╚═╝╚═╝" << endl;
            cout << "██║     ███████╗██║  ██║██████╔╝██║███████║   ██║   ███████╗██╗██╗" << endl;
            cout << "╚═╝     ╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝" << endl;
                                                                

            cout<<"La palabra era: "<<palabra<<endl;
    }
    if (adivinar=="lealtad"){
        cout<<"La que te falta rey"<<endl;
    }
}







// Funciones del ta te ti
const char JUGADOR_X = 'X';
const char JUGADOR_O = 'O';
const char VACIO = ' ';

char tablero[3][3];
bool es_jugadorX = true;

void inicializar_tablero() { // Genera tablero vacio
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) { 
            tablero[i][j] = VACIO;
        }
    }
}

void mostrar_tablero() {
   cout << "    0    1    2" << endl; // Muestra la posicion de cada columna y fila
    for (int i = 0; i < 3; i++) {
        cout <<i<< "|";
        for (int j = 0; j < 3; j++) {
            cout << tablero[i][j] <<"__ |"; // Genera los espaicos vacios
        }
        cout << endl;
    }
}

bool si_el_movimiento_es_valido(int fila, int columna) {    // Verifica que ingreses las columnas y filas correctas
    return (fila >= 0 && fila < 3 && columna >= 0 && columna < 3 && tablero[fila][columna] == VACIO);
}

bool hay_ganador() { // Verifico todas las combinaciones posibles de hacer tres en linea
    for (int i = 0; i < 3; i++) {
        if (tablero[i][0] != VACIO && tablero[i][0] == tablero[i][1] && tablero[i][1] == tablero[i][2]) {
            return true;
        }
    }

    // Verificar columnas
    for (int j = 0; j < 3; j++) {
        if (tablero[0][j] != VACIO && tablero[0][j] == tablero[1][j] && tablero[1][j] == tablero[2][j]) {
            return true;
        }
    }

    // Verificar diagonales
    if (tablero[0][0] != VACIO && tablero[0][0] == tablero[1][1] && tablero[1][1] == tablero[2][2]) {
        return true;
    }
    if (tablero[0][2] != VACIO && tablero[0][2] == tablero[1][1] && tablero[1][1] == tablero[2][0]) {
        return true;
    }

    return false;
}
// Verificamos si hay empate
bool empate() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (tablero[i][j] == VACIO) {
                return false;
            }
        }
    }
    return true;
}

// Juego en si

void tic_tac_toe (){
    inicializar_tablero();

    while (true) {
        mostrar_tablero();

        int fila, columna;
        cout << "Jugador " << (es_jugadorX ? JUGADOR_X : JUGADOR_O) << ", ingrese la fila y la columna (0-2): ";
        cin >> fila >> columna;

        if (!si_el_movimiento_es_valido(fila, columna)) {
            cout << "Movimiento inválido. Intente nuevamente." << endl;
            continue;
        }

        tablero[fila][columna] = es_jugadorX ? JUGADOR_X : JUGADOR_O;
        es_jugadorX = !es_jugadorX;

        if (hay_ganador()) {
            mostrar_tablero();
            cout << "¡El jugador " << (es_jugadorX ? JUGADOR_O : JUGADOR_X) << " ha ganado!" << endl;
            break;
        }

        if (empate()) {
            mostrar_tablero();
            cout << "██╗███████╗███╗   ███╗██████╗  █████╗ ████████╗███████╗██╗" << endl;
            cout << "██║██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║" << endl;
            cout << "██║█████╗  ██╔████╔██║██████╔╝███████║   ██║   █████╗  ██║" << endl;
            cout << "╚═╝██╔══╝  ██║╚██╔╝██║██╔═══╝ ██╔══██║   ██║   ██╔══╝  ╚═╝" << endl;
            cout << "██╗███████╗██║ ╚═╝ ██║██║     ██║  ██║   ██║   ███████╗██╗" << endl;
            cout << "╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝" << endl;
            break;
        }
    }


}



// Funciones de la generala
// Creo un vector de 5 elementos
bool generala(vector<int> dados) {
    return count(dados.begin(), dados.end(), dados[0]) == 5;
}
// Verifico si hay poker
bool poker(vector<int> dados) {
    sort(dados.begin(), dados.end());
    return count(dados.begin(), dados.end(), dados[0]) == 4 || count(dados.begin(), dados.end(), dados[4]) == 4;
}
// Verifico si hay full

bool full(vector<int> dados) {
    sort(dados.begin(), dados.end());
    return (count(dados.begin(), dados.end(), dados[0]) == 3 && count(dados.begin(), dados.end(), dados[4]) == 2) ||
    (count(dados.begin(), dados.end(), dados[0]) == 2 && count(dados.begin(), dados.end(), dados[3]) == 3);
}
// Verifico si hay escalera
bool escalera(vector<int> dados) {
    sort(dados.begin(), dados.end());
    for (int i = 0; i < dados.size() - 4; i++) {
        if (dados[i] == dados[i + 1] - 1 && dados[i + 1] == dados[i + 2] - 1 && dados[i + 2] == dados[i + 3] - 1 && dados[i + 3] == dados[i + 4] - 1) {
            return true;
        }
    }
    return false;
}
// Cambio de manera random los elementos del vector dados
vector<int> tirar_dados() {
    vector<int> dados(5);
    for (int i = 0; i < 5; i++) {
        dados[i] = rand() % 6 + 1;
    }
    return dados;
}
void jugar_ronda() {
    vector<int> dados = tirar_dados(); // tiro los dados
    char opcion;
    bool jugada_especial = false;
    map<int, int> numeros;
    int intentos = 0;
    const int MAX_INTENTOS = 3;

    // Juego en si
    do {
        // Muestro los elementos del vector dados
        cout << "Dados: ";
        for (int i = 0; i < dados.size(); i++) {
            cout << dados[i] << " ";
            numeros[dados[i]]++;
        }
        cout << endl;

        if (generala(dados)) {
            cout << "¡Generala!" << endl;// Juego en si

            jugada_especial = true;
        } else if (poker(dados)) {
            cout << "¡Poker!" << endl;
            jugada_especial = true;
        } else if (full(dados)) {
            cout << "¡Full!" << endl;
            jugada_especial = true;
        } else if (escalera(dados)) {
            cout << "¡Escalera!" << endl;
            jugada_especial = true;
        } else {                    // Verifico si se repiten numeros, en el caso de que si, los sumo y lo muestro, sino sigo
            bool hay_repetidos = false;
            for (auto par : numeros) {
                if (par.second > 1) {
                    cout << "Suma de " << par.first << ": " << par.first * par.second << endl;
                    hay_repetidos = true;
                }
            }
            if (!hay_repetidos) {
                cout << "No hay números repetidos." << endl;
            }
        }

        intentos++;

        if (intentos >= MAX_INTENTOS) { // Verifico si hice tres intentor
            cout << "Se alcanzó el máximo de intentos. Iniciando una nueva ronda." << endl;
            break;
        } else if (!jugada_especial) { // Si no hay jugada especial (poker, escalera, full, generala) imprimo lo siguiente
            cout << "No hubo ninguna jugada especial. Intento " << intentos << "/" << MAX_INTENTOS << "." << endl;
            cout << "¿Deseas volver a tirar algunos dados? (s/n): ";
            cin >> opcion;
            if (opcion == 's' || opcion == 'S') {
                string dados_a_tirar;
                cout << "Ingresa los números de los dados que deseas volver a tirar (separados por espacios, o 'todos' para volver a tirar todos los dados): ";
                cin >> dados_a_tirar;
                // Si quiere volver a tirar le pido que me indicque la posicion en la que se encuentra en el vector el dado que quiere volver a tirar o en el caso de que quiera tirar todos devuelta escriba todos en la terminal
                if (dados_a_tirar == "todos") {
                    dados = tirar_dados();
                } else {
                    istringstream iss(dados_a_tirar); 
                    vector<int> indices;
                    int indice;
                    while (iss >> indice) {
                        if (indice >= 1 && indice <= 5) {
                            indices.push_back(indice - 1);
                        }
                    }
                    vector<int> nuevos_dados = tirar_dados(); // Tirar nuevos dados
                    for (int i = 0; i < dados.size(); i++) {
                        if (find(indices.begin(), indices.end(), i) == indices.end()) {
                            nuevos_dados[i] = dados[i]; // Mantener los dados no seleccionados
                        }
                    }
                    dados = nuevos_dados; // Reemplazar los dados con los nuevos dados
                }
                numeros.clear();
            } else {
                break;
            }
        } else {
            cout << "¿Deseas intentar mejorar la jugada? Intento " << intentos << "/" << MAX_INTENTOS << " (s/n): ";
            cin >> opcion;
            if (opcion == 's' || opcion == 'S') {
                dados = tirar_dados();
                numeros.clear();
            } else {
                break;
            }
        }
    } while (intentos < MAX_INTENTOS && (opcion == 's' || opcion == 'S'));
}

// Juego en si

void generala() {
    srand(time(NULL)); // Lo utilizo para inicializar la biblioteca que genera numeros random
    char opcion;
    do {
        jugar_ronda();
        cout << "Presiona s para jugar otra ronda, o q para salir: ";
        cin >> opcion;
    } while (opcion != 'q');
}


// Muestro el menu


void mostrarMenu() {
    cout << "------ MENÚ ------" << endl;
    cout << "1 Tic Tac Toe" << endl;
    cout << "2 Generala" << endl;
    cout << "3 Ahorcado" << endl;
    cout << "4 Salir" << endl;
    cout << "------------------" << endl;
    cout << "Seleccione una opción: ";
}

int main() {
    int opcion;
    float n1;
    float n2;

    
    mostrarMenu();
    
    cin >> opcion;

    while (opcion!=4) {
        switch (opcion) {
            case 1:
                cout << "Tic tac toe" << endl;
                tic_tac_toe();
                break;
            case 2:
                cout << "Generala" << endl;
                generala();
                break;
            case 3:
                cout << "Ahorcado" << endl;
                ahorcado();
                break;
            
                
            default:
                cout << "Opción no válida" << endl;
                break;
        }
        
        mostrarMenu();
        cin >> opcion;
    }

    cout << "Saliendo del menú.." << endl;

}