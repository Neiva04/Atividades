#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// Definição da estrutura do nó da lista de adjacências
typedef struct Node {
    int vertex;
    struct Node* next;
} Node;

// Função para criar um novo nó da lista de adjacências
Node* createNode(int v) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}

// Função para exibir a lista de adjacências
void printAdjList(Node** adjList, int n) {
    for (int i = 0; i < n; i++) {
        Node* curr = adjList[i];
        printf("Adjacencias do vertice %d (%c): ", i, i + 'A');
        while (curr != NULL) {
            printf("%c ", curr->vertex + 'A');
            curr = curr->next;
        }
        printf("\n");
    }
}

int main() {
    FILE* file = fopen("grafo.txt", "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return 1;
    }

    char vertexLabels[100][100];
    int n = 0;

    // Leitura dos rótulos dos vértices
    fscanf(file, "%s", vertexLabels[n]);
    n++;

    // Armazenamento dos rótulos dos vértices em um vetor
    char* token = strtok(vertexLabels[0], " ");
    while (token != NULL) {
        token = strtok(NULL, " ");
        if (token != NULL) {
            strcpy(vertexLabels[n], token);
            n++;
        }
    }

    // Criação da lista de adjacências
    Node** adjList = (Node**)malloc(n * sizeof(Node*));
    for (int i = 0; i < n; i++) {
        adjList[i] = NULL;
    }

    // Leitura da matriz de adjacências e armazenamento na lista de adjacências
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int value;
            fscanf(file, "%d", &value);
            if (value == 1) {
                Node* newNode = createNode(j);
                newNode->next = adjList[i];
                adjList[i] = newNode;
            }
        }
    }

    // Exibição da lista de adjacências
    printAdjList(adjList, n);

    fclose(file);
    return 0;
}
