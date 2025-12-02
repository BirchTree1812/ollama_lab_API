# Explanation
The purpose of this task is to design a quick FastAPI application that pulls up a LLM on the user's computer to answer different queries.

# Instructions

Before running, ensure that:
+ Ollama is installed on your computer
  + at least one local LLM is installed on Ollama 
+ you can successfully run `ollama serve`
+ ports 8000(default FastAPI port) and 11434(default Ollama port) are not occupied
  + if they are occupied by another process, then you can:
    + abort those processes
    + change the ports.
      + For the FastAPI port, change it to another value(i.e. 8001).
      + For the Ollama port, run the `OLLAMA_HOST=127.0.0.1:<port value> ollama serve`, where <port value> is your chosen alternative value of the port