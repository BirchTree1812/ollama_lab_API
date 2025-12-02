# Explanation
The purpose of this task is to design a quick FastAPI application that pulls up a LLM on the user's computer to answer different queries.

# Instructions

## Preparation

Before running, ensure that:
+ Ollama is installed on your computer
  + at least one local LLM is installed on Ollama 
+ you can successfully run `ollama serve`
+ ports 8000(default FastAPI port) and 11434(default Ollama port) are not occupied
  + if they are occupied by another process, then you can:
    + abort those processes
      + check by running `sudo lsof -i :8000`. One of the results will be a PID
      + then run kill -9 <PID>, where <PID> is the process ID of the process that's occupying the port you want to free
    + change the ports.
      + For the FastAPI port, change it to another value(i.e. 8001).
      + For the Ollama port, run the `OLLAMA_HOST=127.0.0.1:<port value> ollama serve`, where <port value> is your chosen alternative value of the port


When you run it, go to the address http://127.0.0.1:8000/docs. There, you should see the title "Ollama CSV Analyzer" with several dropdown headings. They represent API calls, which will be discussed in the next section.

## FastAPI Calls

API calls allow the user to execute different functions. In this case, this means that the local LLM summoned by Ollama to the FastAPI app will execute queries given by the user.

+ /generate - takes a simple text query, gives out a response
+ /analyze_csv - takes a simple text query and a .csv file, gives out a response. The maximum file size acceptable depends on the size of the LLM loaded and the consumption of RAM/VRAM by other processes of this machine.
+ /health - checks whether Ollama is capable of running a query

# Conclusion

This app can run 