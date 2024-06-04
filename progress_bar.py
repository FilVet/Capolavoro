from sys import stdout

# Funzione che disegna barra
def show_progress_bar (current_value, total_value,*, character = "█", length_bar = 50):
    percentual_complete = (current_value/total_value) * 100                                     # Calcolo percentuale completamento
    filled = int(length_bar * current_value // total_value)                                     # Calcolo numero di characters da mettere
    bar = filled*character + '-'*(length_bar - filled)                                          # Barra in sé
    stdout.write(f'\r|{bar}| {percentual_complete:0.2f}% ')                                     # Disegno barra
    stdout.flush()                                                                              # Velocizza visualizzazione barra
    
if __name__ == "__main__":                                                                      # Test
    from time import sleep
    total = 100
    for i in range(0, total+1):
        show_progress_bar(i, total, length_bar=30)
        sleep(.1)
    