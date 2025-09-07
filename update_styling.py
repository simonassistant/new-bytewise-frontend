import re

with open('src/views/Chat.vue', 'r') as f:
    content = f.read()

# Replace the ternary operator with object-based class binding
old_line = "              msg.role === 'user'"
new_content = '''            :class="{
              'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none': msg.role === 'user',
              'bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none': msg.role === 'assistant' && !msg.openRouter,
              'bg-gradient-to-r from-yellow-400 to-orange-500 text-black rounded-bl-none border-2 border-yellow-600': msg.role === 'assistant' && msg.openRouter
            }"'''

# Find and replace the class binding section
lines = content.split('\n')
for i, line in enumerate(lines):
    if "msg.role === 'user'" in line and ":class=" in lines[i-1]:
        # Replace the next 3 lines (the ternary operator)
        lines[i-1:i+2] = [new_content]
        break

content = '\n'.join(lines)

with open('src/views/Chat.vue', 'w') as f:
    f.write(content)

print('Updated message styling for OpenRouter messages')
