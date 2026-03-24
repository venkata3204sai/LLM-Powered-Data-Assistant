from ollama import chat
from ollama import Client
import pandas as pd

client = Client(host='http://localhost:11434')
df = pd.read_csv("twitchdata-update.csv")
df.columns = df.columns.str.strip()
models = ["llama3.2", "gemma:7b"]

def generate_query(model, query):
    schema = str(df.columns.tolist())
    sample = str(df.iloc[0].to_dict())

    prompt = f"""
    You are a data assistant that converts questions into pandas queries.
 
    Dataset columns: {schema}
    Sample row: {sample}
 
    STRICT RULES:
    - Only return ONE line of pandas code
    - Do NOT include import statements
    - Do NOT include explanations
    - Do NOT assign to variables
    - Assume the DataFrame is named df
    - The result must ALWAYS be a DataFrame with ALL columns
    - If ANY requested field is not exactly present in the dataset columns, return exactly: ERROR: Column not found
    - DO NOT guess, map, infer, or substitute similar columns under any condition
 
    EXAMPLES:
    Q: streamer with highest average viewers
    A: df[df['Average viewers'] == df['Average viewers'].max()]
 
    Q: top 5 streamers by followers gained
    A: df.nlargest(5, 'Followers gained')
 
    Return ONLY the pandas code. Nothing else.
    """

    response = client.chat(
        model = model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}],
        options={"temperature": 0}
    )

    pandas_query = str(response.message.content)
    pandas_query = pandas_query.replace("```python", "").replace("```", "").replace("`", "").strip()
    return pandas_query

def execute_query(query):
    try:
        result = eval(query, {"__builtins__": {}}, {"df": df})
        if isinstance(result, pd.Series):
            result = result.to_frame().T
        elif not isinstance(result, pd.DataFrame):
            result = pd.DataFrame({"Result": [result]})
        return result
    except KeyError as e:
        print(f"Error: Column {e} not found. Available columns: {', '.join(df.columns.tolist())}")
        return None
    except Exception as e:
        print("Error:", e)
        return None

def summarize(model, query, result):
    summary = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are a data analyst. Provide short summaries with key insights. Keep it concise."},
            {"role": "user", "content": f'I asked: "{query}"\n\nHere is the data:\n{result.head(10).to_string(index=False)}'}
        ])
    
    return summary.message.content

def compare_results(summaries):
    system_prompt = "You are a senior data analyst. Compare two AI answers. If they agree, state the consensus. If they conflict, explain the discrepancy and give a unified answer."

    user_prompt = f"""
    Assistant A ({models[0]}) said: {summaries[models[0]]}
 
    Assistant B ({models[1]}) said: {summaries[models[1]]}
    """
    comparison = client.chat(
        model=models[0],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return comparison.message.content

def main():
    print("\nWelcome to the ChatBot!!!")
    print("="*50 + "\n")
    print(f"""
    This data contains Top 1000 Streamers from past one year who were streaming on twitch.
    You can ask about viewer counts, stream time, followers gained and more.
    
    Columns: {', '.join(df.columns.tolist())}
    """)
    print("="*50 + "\n")

    while True:
        query = input("\nWhat specific data are you looking for? (or 'q' to exit): ").strip()
        if query.lower() == 'q':
            print("Goodbye!!!")
            break

        summaries = {}
        too_many = False
        
        for model in models:
            print("\n" + "-"*50)
            print(f"--- {model} ---")
            pandas_query = generate_query(model, query)
            print("Generated Query:", pandas_query)
            result = execute_query(pandas_query)
            if result is None:
                print(f"{model} failed to produce a valid query.")
                summaries[model] = None
                continue
            if isinstance(result, pd.DataFrame) and result.shape[0] > 10:
                print("Too many results. Please refine your query.")
                too_many = True
                break
            print("\nRaw Data:")
            print(result.to_string(index=False))
            summary = summarize(model, query, result)
            print("\nSummary:", summary)
            summaries[model] = summary

        if too_many:
            continue
        if all(summaries.values()):
            print("\n" + "-"*50)
            print("\nComparison & Resolution:")
            print(compare_results(summaries))

if __name__ == "__main__":
    main()