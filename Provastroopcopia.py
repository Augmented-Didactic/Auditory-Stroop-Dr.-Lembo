import os
import random
import time
import subprocess

# Percorso della cartella "compressed" sul desktop
compressed_folder = os.path.join(os.path.expanduser("~"), "Desktop", "compressed")

# Lista dei file audio presenti nella cartella "compressed"
audio_files = [file for file in os.listdir(compressed_folder) if file.endswith(".wav")]

# Definizione delle istruzioni audio
instruction1_path = os.path.join(compressed_folder, "instruction1.wav")
instruction2_path = os.path.join(compressed_folder, "instruction2.wav")

# Funzione per riprodurre le istruzioni audio
def play_instruction(instruction_path):
    subprocess.run(["afplay", instruction_path])  # Riproduzione dell'audio

# Esecuzione delle istruzioni audio
play_instruction(instruction1_path)
play_instruction(instruction2_path)

# Definizione delle istruzioni testuali
instructions = [
    "Premi 'I' se lo stimolo è incongruente, 'C' se lo stimolo è congruente.",
    "Ascolta il nome e indica se il genere del nome coincide con la voce che lo pronuncia."
]

# Funzione per eseguire il task di Stroop
def stroop_task(trials):
    correct_trials = 0
    response_times_congruent = []
    response_times_incongruent = []
    start_time = time.time()
    for i in range(trials):
        # Randomizzazione degli stimoli congruenti e incongruenti
        congruent = random.choice([True, False])
        congruent_files = [file for file in audio_files if file.startswith("Congruente")]
        incongruent_files = [file for file in audio_files if file.startswith("Incongruente")]
        if congruent:
            audio_file = random.choice(congruent_files)
        else:
            audio_file = random.choice(incongruent_files)
        print("Ascolta il nome:")
        play_start_time = time.time()
        subprocess.run(["afplay", os.path.join(compressed_folder, audio_file)])  # Riproduzione dell'audio
        play_end_time = time.time()
        response = input("Congruente (C) o Incongruente (I): ").upper()
        response_time = time.time() - play_end_time
        if congruent:
            response_times_congruent.append(response_time)
        else:
            response_times_incongruent.append(response_time)
        if (congruent and response == 'C') or (not congruent and response == 'I'):
            print("Corretto!")
            correct_trials += 1
        else:
            print("Sbagliato.")
        time.sleep(1)  # Ritardo tra le prove
    end_time = time.time()
    return correct_trials, response_times_congruent, response_times_incongruent, end_time - start_time

# Esecuzione dell'esperimento
print("Benvenuto all'esperimento di Stroop!")
for instruction in instructions:
    print(instruction)
    input("Premi Invio per continuare...")
num_trials = 15
correct, response_times_congruent, response_times_incongruent, duration = stroop_task(num_trials)
print(f"Hai completato {num_trials} prove in {duration:.2f} secondi.")
print(f"Percentuale di risposte corrette: {correct / num_trials * 100:.2f}%")
print("Tempi di risposta per gli stimoli congruenti:")
for i, time in enumerate(response_times_congruent):
    print(f"Stimolo congruente {i+1}: {time:.2f} secondi")
print("Tempi di risposta per gli stimoli incongruenti:")
for i, time in enumerate(response_times_incongruent):
    print(f"Stimolo incongruente {i+1}: {time:.2f} secondi")
