import numpy as np

class KnapsackGA:
    def __init__(self, weights, values, capacity, pop_size=100, generations=100):
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.capacity = capacity
        self.pop_size = pop_size
        self.generations = generations

    def initialize_population(self):
        return np.random.randint(2, size=(self.pop_size, len(self.weights)))

    def fitness(self, individual):
        total_weight = np.sum(individual * self.weights)
        if total_weight > self.capacity:
            return 0  # Soluzione non valida
        return np.sum(individual * self.values)

    def selection(self, population):
        fitnesses = np.array([self.fitness(ind) for ind in population])
        return population[np.argsort(fitnesses)[-self.pop_size//2:]]
    
    def tournament_selection(self, population, k=3):
        n_parents = self.pop_size // 2
        selected_indices = []
        all_fitnesses = np.array([self.fitness(ind) for ind in population])
        for _ in range(n_parents):
            competitors_idx = np.random.choice(len(population), k, replace=False)
            competitors_fitnesses = all_fitnesses[competitors_idx]
            winner_local_idx = np.argmax(competitors_fitnesses)
            winner_global_idx = competitors_idx[winner_local_idx]
            selected_indices.append(winner_global_idx)
        winners_population = population[selected_indices]
        winners_fitnesses = all_fitnesses[selected_indices]
        sorted_indices = np.argsort(winners_fitnesses)
        
        return winners_population[sorted_indices]
    
    def crossover(self, parent1, parent2):
        crossover_point = np.random.randint(len(parent1))
        child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
        return child1, child2
    
    def uniform_crossover(self, parent1, parent2):
        # genero un array (numeri compresi tra 0 e 1) -> tutti quelli maggiori 0.5 diventano 0 (false) e quelli minori 1 (true)
        mask = np.random.rand(len(parent1)) < 0.5
        # se la maschera è True prende da parent1, altrimenti da parent2
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2

    def mutation(self, individual, mutation_rate=0.01):
        return np.where(np.random.random(len(individual)) < mutation_rate, 1 - individual, individual)

    def mutation_swap(self, individual, mutation_rate=0.01): #togliamo un oggetto e ne inseriamo un altro
        if np.random.random() < mutation_rate:
            idx_in = np.where(individual == 1)[0]
            idx_out = np.where(individual == 0)[0]
            
            if len(idx_in) > 0 and len(idx_out) > 0:
                to_remove = np.random.choice(idx_in)
                to_add = np.random.choice(idx_out)
                individual[to_remove] = 0
                individual[to_add] = 1
                
        return individual
    def evolve(self, n_elites =2):
        population = self.initialize_population()
        for _ in range(self.generations):
            population = self.tournament_selection(population) #generata in ordine ASC di fitness
            elite_population = population[-n_elites:]
            new_population = []
            probs = ramp_selection_probs(len(population))
            for _ in range((self.pop_size - n_elites) // 2): #abbasso il numero di giri del numero di tuple messe da parte
                parent1, parent2 = population[np.random.choice(len(population), 2, replace=False, p=probs)] #rendo più probabile la scelta di parent più efficienti
                child1, child2 = self.uniform_crossover(parent1, parent2)
                new_population.extend([self.mutation_swap(child1), self.mutation_swap(child2)])
            new_population.extend(elite_population)
            population = np.array(new_population)
        best_solution = max(population, key=self.fitness)
        return self.refine_solution(best_solution, self.fitness(best_solution))
    
    def refine_solution(self, best_solution, fitness):
        sol = best_solution.copy()
        current_value = fitness
        current_weight = sol @ self.weights #equivale a sum ( sol * weights)
             
        def find_best_add():
            remaining_cap = self.capacity - current_weight
            
            # Prendo solo chi è a 0 (fuori) e il cui peso entra nello spazio rimasto
            valid_mask = (sol == 0) & (self.weights <= remaining_cap)
            
            # Estraggo gli INDICI originali dove la maschera è True (1)
            valid_indices = np.flatnonzero(valid_mask)
            
            if valid_indices.size == 0:
                return 0, -1
                
            valid_values = self.values[valid_indices] #risalgo ai valori validi tramite gli indici
            best_pos = np.argmax(valid_values) #estraggo l'indice relativo del valore massimo (in valid_values)
            
            best_idx = valid_indices[best_pos] #converto l'indice relativo nell'indice valido
            best_gain = valid_values[best_pos] #estraggo il valore
            
            return best_gain, best_idx
        
        def find_best_swap():
            in_indices = np.flatnonzero(sol == 1)
            out_indices = np.flatnonzero(sol == 0)
            
            # Se lo zaino è vuoto o pieno, o non ci sono oggetti fuori, esco subito
            if in_indices.size == 0 or out_indices.size == 0:
                return 0, -1, -1
                
            # Trasformo gli array degli elementi "IN" in Vettori Colonna (aggiungendo un asse)
            w_in = self.weights[in_indices][:, np.newaxis] #equivale arr.reshape(-1, 1) mette in colonna l'array, altero la forma dell'array ":" prende tutti gli elementi che ci sono in questa dimensione "," passo alla dimensione successiva "np.newaxis" crea un nuovo asse
            v_in = self.values[in_indices][:, np.newaxis]
            
            # Lascio gli array degli elementi "OUT" come Vettori Riga normali
            w_out = self.weights[out_indices]                
            v_out = self.values[out_indices]                 
            
            # Qui NumPy incrocia in automatico colonne e righe!
            new_weights = current_weight - w_in + w_out #numpy espande implicitamente le dimensioni degli array sui loro valori per rendere possibile la somma/sottrazione
            gains = v_out - v_in
            
            # Trovo dove il peso è valido E il guadagno è maggiore di 0
            valid_mask = (new_weights <= self.capacity) & (gains > 0)
            
            if not np.any(valid_mask):
                return 0, -1, -1 # Nessuno scambio valido migliora la situazione
                
            # Sostituisco i guadagni non validi con -1 per escluderli dalla ricerca
            masked_gains = np.where(valid_mask, gains, -1)
            
            # Trovo la posizione "piatta" del guadagno massimo assoluto nella griglia
            best_flat_pos = np.argmax(masked_gains)
            
            # Converto la posizione "piatta" nelle coordinate originali (riga, colonna)
            row_pos, col_pos = np.unravel_index(best_flat_pos, masked_gains.shape)
            
            best_gain = masked_gains[row_pos, col_pos]
            
            #la riga corrisponde all'indice in "in_indices",  la colonna corrisponde all'indice in "out_indices"
            best_out = in_indices[row_pos]
            best_in = out_indices[col_pos]
            
            return best_gain, best_out, best_in

        
        improved = True
        while improved:
            improved = False
            
            add_gain, add_idx = find_best_add()
            swap_gain, swap_out, swap_in = find_best_swap()
            
            if add_gain <= 0 and swap_gain <= 0:
                break
                
            if add_gain >= swap_gain:
                sol[add_idx] = 1
                current_weight += self.weights[add_idx]
                current_value += add_gain
            else:
                sol[swap_out] = 0
                sol[swap_in] = 1
                current_weight = current_weight - self.weights[swap_out] + self.weights[swap_in]
                current_value += swap_gain
                
            improved = True

        return sol, current_value
        
def ramp_selection_probs(size, slope = 0.1):
    base_prob = 1.0/size
    base_array = np.full(size, base_prob)
    delta_array = np.linspace(-slope * base_prob, slope * base_prob, size)
    return base_array + delta_array


# Esempio di utilizzo
weights = [10, 20, 30, 40, 50]
values = [60, 100, 120, 180, 300]
capacity = 100
ga = KnapsackGA(weights, values, capacity)
best_solution, best_value = ga.evolve()
print(f"---------Giro1.0---------")
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

ga = KnapsackGA(weights, values, capacity, generations=500)
best_solution2, best_value2 = ga.evolve()
print(f"---------Giro1.1---------5x generations")
print(f"Soluzione migliore: {best_solution2}")
print(f"Valore totale: {best_value2}")
print(f"Peso totale: {np.sum(best_solution2 * weights)}")

ga = KnapsackGA(weights, values, capacity, generations=20)
best_solution3, best_value3 = ga.evolve()
print(f"---------Giro1.2---------0.2x generations")
print(f"Soluzione migliore: {best_solution3}")
print(f"Valore totale: {best_value3}")
print(f"Peso totale: {np.sum(best_solution3 * weights)}")


print(f"---------Giro2.0---------")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=200,generations=500)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.1--------- 0.2x generations")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=200,generations=100)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.2--------- 0.2x pop_size")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=40,generations=500)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.3--------- 0.2x generations 0.2x pop_size")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=40,generations=100)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.4--------- 0.1x generations 0.1x pop_size")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=20,generations=50)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.5--------- 2x generations 2x pop_size")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=400,generations=1000)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")

print(f"---------Giro2.6--------- 0.05x generations 0.05x pop_size")
weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
values = [60, 100, 120, 180, 300, 310, 330, 350, 400, 450]
capacity = 400
ga = KnapsackGA(weights, values, capacity, pop_size=10, generations=25)
best_solution, best_value = ga.evolve()
print(f"Soluzione migliore: {best_solution}")
print(f"Valore totale: {best_value}")
print(f"Peso totale: {np.sum(best_solution * weights)}")