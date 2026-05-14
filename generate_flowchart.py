import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(7, 11))
ax.axis('off')

steps = [
    '1. Start',
    '2. User Inputs Car Details',
    '3. Send Data to API (FastAPI)',
    '4. API Preprocesses Data',
    '5. Model Predicts Price (Random Forest)',
    '6. Log Query to Database (SQLite)',
    '7. Return Price & Insights',
    '8. Display Dashboard & Generate PDF',
    '9. End'
]

y_pos = 0.95
for i, step in enumerate(steps):
    ax.text(0.5, y_pos, step, ha='center', va='center', size=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f2fe', edgecolor='#0284c7', linewidth=2))
    
    if i < len(steps) - 1:
        ax.annotate('', xy=(0.5, y_pos - 0.08), xytext=(0.5, y_pos - 0.02),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#0ea5e9'))
    
    y_pos -= 0.1

plt.savefig('CarVal_Flowchart.png', bbox_inches='tight', dpi=300)
print("Saved CarVal_Flowchart.png successfully!")
