import anthropic
from rich import print as rprint
from datetime import datetime
from zoneinfo import ZoneInfo

client = anthropic.Anthropic()
conversation_history = []

INPUT_PRICE = 0.10
OUTPUT_PRICE = 0.50

def get_current_time_for_zone(zone):
    return datetime.now(ZoneInfo(zone)).strftime("%H:%M:%S")

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")



GET_TIME_TOOL = {
    "name": "get_current_time",
    "description": "Returns the current local time (Europe/Sofia) as HH:MM:SS. "
                   "Use when the user asks what time it is.",
    "input_schema": {"type": "object", "properties": {}, "required": []},
}

GET_ZONE_INFO_TOOL = {
    "name": "get_current_time_for_zone",
    "description": "Returns the current zone time as HH:MM:SS. "
                   "Use when the user asks what time it is for a specific zone",
    "input_schema": {"type": "object", "properties": {"zone": {"type": "string","description": "The zone for which to get the current time""IANA timezone name, e.g. 'Europe/London', 'Asia/Tokyo', 'America/New_York'"}}, "required": ["zone"]},
}

TOOL_FUNCTIONS = {"get_current_time": get_current_time, "get_current_time_for_zone": get_current_time_for_zone}


def ask_claude(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    while True:

        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=300,
            system="You are a concise assistant.",
            messages=conversation_history,
            tools=[GET_TIME_TOOL,GET_ZONE_INFO_TOOL],
        )
        conversation_history.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return response


        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                rprint(f"[yellow]→ Claude wants: {block.name}({block.input})[/yellow]")

                function = TOOL_FUNCTIONS[block.name]

                try:
                    result = function(**block.input)
                    is_error = False
                except Exception as e:
                    result = f"Error: {e}"
                    is_error = True

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,   # links this result to Claude's request
                    "content": result,
                })


        conversation_history.append({"role": "user", "content": tool_results})


if __name__ == '__main__':
    for i in range(3):
        question = input("What is the question? ")
        response = ask_claude(question)

        for block in response.content:
            if block.type == "text":
                print(block.text)

        input_cost = response.usage.input_tokens / 1_000_000 * INPUT_PRICE
        output_cost = response.usage.output_tokens / 1_000_000 * OUTPUT_PRICE
        rprint(f"[dim]Cost of last call: ${input_cost + output_cost:.6f}[/dim]")