from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

trial3Json = {
  "nodes": [
    {
      "id": "ChatInput-xyz789",
      "type": "genericNode",
      "position": { "x": 250, "y": 300 },
      "data": {
        "type": "ChatInputComponent",
        "id": "ChatInput-xyz789",
        "node": {
          "display_name": "Chat Input",
          "description": "Get chat inputs from the Playground.",
          "base_classes": ["Message"],
          "template": {
            "input_value": {
              "type": "str",
              "display_name": "Text",
              "value": "Hello",
              "info": "Message to be passed as input."
            },
            "sender": {
              "type": "str", 
              "value": "User",
              "options": ["Machine", "User"]
            }
          }
        }
      }
    },
    {
      "id": "OpenAIModel-abc123",
      "type": "OpenAIModel",
      "position": { "x": 500, "y": 300 },
      "data": {
        "type": "OpenAIModelComponent",
        "id": "OpenAIModel-abc123",
        "node": {
          "display_name": "OpenAI",
          "description": "Generates text using OpenAI LLMs.",
          "base_classes": ["LanguageModel"],
          "template": {
            "api_key": {
              "type": "str",
              "required": True,
              "display_name": "OpenAI API Key",
              "value": ""
            },
            "model_name": {
              "type": "str",
              "required": True,
              "display_name": "Model Name",
              "value": "gpt-4o"
            },
            "temperature": {
              "type": "float",
              "required": False,
              "display_name": "Temperature",
              "value": 0.1
            },
            "input_value": {
              "type": "str",
              "display_name": "Input",
              "value": ""
            },
            "system_message": {
              "type": "str",
              "display_name": "System Message",
              "value": ""
            }
          }
        }
      }
    }
  ],
  "edges": [
    {
      "id": "edge-ChatInput-xyz789-to-OpenAIModel-abc123",
      "source": "ChatInput-xyz789",
      "target": "OpenAIModel-abc123",
      "sourceHandle": "{œdataTypeœ:œChatInputComponentœ,œidœ:œChatInput-xyz789œ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}",
      "targetHandle": "{œfieldNameœ:œinput_valueœ,œidœ:œOpenAIModel-abc123œ,œinputTypesœ:[œMessageœ],œtypeœ:œstrœ}",
      "data": {
        "sourceHandle": {
          "dataType": "ChatInputComponent",
          "id": "ChatInput-xyz789",
          "name": "message", 
          "output_types": ["Message"]
        },
        "targetHandle": {
          "fieldName": "input_value",
          "id": "OpenAIModel-abc123",
          "inputTypes": ["Message"],
          "type": "str"
        }
      }
    }
  ]
}

trial2Json = {
  "nodes": [
      {
      "id": "node-1",
      "type": "ChatInput", # This can be either "ChatInput" or "genericNode" with type: "ChatInput" in data
      "position": { "x": 100, "y": 100 },
      "data": {
        "label": "Chat Input Node",
        "type": "ChatInput",
        "id": "node-1",
        "node": {
          "template": {
            "input_text": {
              "type": "string",
              "value": "Hello, how can I help you?"
            },
            "input_value": {  # This is the critical field that creates the text input
              "type": "string",
              "value": "",
              "display_name": "Text",
              "multiline": True
            },
            "should_store_message": {
              "type": "boolean",
              "value": True
            },
            "sender": {
              "type": "string",
              "value": "User"
            }
          },
          "description": "Get chat inputs from the Playground.",
          "icon": "MessagesSquare",
          "base_classes": ["Message"],
          "display_name": "Chat Input",
          "outputs": [
            {
              "types": ["Message"],
              "selected": "Message",
              "name": "message",
              "display_name": "Message",
              "method": "message_response",
              "value": "__UNDEFINED__",
              "cache": True,
              "allows_loop": False,
              "tool_mode": True
            }
          ],
          "field_order": ["input_value", "should_store_message", "sender"]
        }
      }
    },
    {
      "id": "node-2",
      "type": "genericNode",
      "position": { "x": 400, "y": 100 },
      "data": {
        "label": "Chat Output Node",
        "type": "ChatOutput",
        "id": "node-2",
        "node": {
          "template": {
            "input_value": {
              "type": "Message",
              "value": "",
              "required": True,
              "display_name": "Input"
            },
            "output_text": {
              "type": "string",
              "value": "Sure, let me assist you with that."
            }
          },
          "description": "Display a chat message in the Playground.",
          "icon": "MessagesSquare",
          "base_classes": ["Message"],
          "display_name": "Chat Output",
          "field_order": ["input_value", "should_store_message"]
        }
      }
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2",
      "type": "smoothstep"
    }
  ]
}

trial1Json = {
    "nodes": [
    {
      "id": "node-1",
      "type": "ChatInput",
      "data": {
        "label": "Chat Input Node",
        "node": {
          "template": {
            "input_text": {
              "type": "string",
              "value": "Hello, how can I help you?"
            }
          }
        }
      },
      "position": { "x": 100, "y": 100 }
    }
    ]
}

def generate_flow_from_use_case(use_case):
    """
    Process the use case with AI and generate an appropriate flow.
    This is a placeholder function - implement with your preferred AI solution.
    
    Args:
        use_case (str): The user's description of their use case
        
    Returns:
        dict: A flow configuration with nodes and edges
    """
    # TODO: Implement AI processing of the use case
    # This would involve:
    # 1. Calling an AI model (OpenAI, LangChain, etc.)
    # 2. Interpreting the use case
    # 3. Generating an appropriate flow configuration
    
    # For now, return a modified version of trial3Json as placeholder
    # In a real implementation, this would be dynamically generated
    modified_flow = trial3Json.copy()
    
    # Example of modifying the flow based on use case
    if "translation" in use_case.lower():
        # Modify for translation use case
        modified_flow["nodes"][1]["data"]["node"]["template"]["system_message"]["value"] = \
            f"You are a translator. Process the following: {use_case}"
    elif "summarization" in use_case.lower():
        # Modify for summarization use case
        modified_flow["nodes"][1]["data"]["node"]["template"]["system_message"]["value"] = \
            f"You are a summarizer. Process the following: {use_case}"
    else:
        # Default modification
        modified_flow["nodes"][1]["data"]["node"]["template"]["system_message"]["value"] = \
            f"Consider this use case: {use_case}"
    
    return modified_flow

@app.route('/api/flows', methods=['GET'])
def return_json():
    # Check if use_case parameter is provided
    use_case = request.args.get('use_case')
    
    if use_case:
        # Generate flow based on the use case
        flow = generate_flow_from_use_case(use_case)
        return jsonify(flow)
    else:
        # Default behavior: return the standard test flow
        return jsonify(trial3Json)

if __name__ == '__main__':
    app.run(debug=True, port=8000)