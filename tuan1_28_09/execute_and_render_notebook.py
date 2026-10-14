import os
import io
import json
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import seaborn as sns
except ImportError:
    sns = None

os.makedirs('images', exist_ok=True)

# Generate fresh notebook
import create_notebook

# Read the notebook
with open('dan_so_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Global execution context
exec_globals = {
    'pd': pd,
    'np': np,
    'plt': plt,
    'sns': sns,
    'os': os
}

chart_counter = 0

for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    code = "".join(cell['source'])
    cell['execution_count'] = cell_idx + 1
    cell['outputs'] = []
    
    # Intercept stdout and plt.show
    old_show = plt.show
    captured_figs = []
    
    def my_show(*args, **kwargs):
        fig = plt.gcf()
        if fig and fig.get_axes():
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode('utf-8')
            captured_figs.append(img_b64)
            
            # Also save to images/
            global chart_counter
            chart_counter += 1
            fig.savefig(f'images/chart_{chart_counter}.png', bbox_inches='tight', dpi=200)
            
            plt.close(fig)
    
    plt.show = my_show
    
    # Run code
    import sys
    old_stdout = sys.stdout
    sys.stdout = stdout_buf = io.StringIO()
    
    try:
        # Check if the code has a display or terminal expression
        exec(code, exec_globals)
        stdout_text = stdout_buf.getvalue()
        
        # Check any un-shown figures
        if plt.get_fignums():
            my_show()
            
        if stdout_text:
            cell['outputs'].append({
                "output_type": "stream",
                "name": "stdout",
                "text": [line + "\n" for line in stdout_text.splitlines()]
            })
            
        for b64 in captured_figs:
            cell['outputs'].append({
                "output_type": "display_data",
                "data": {
                    "image/png": b64,
                    "text/plain": ["<Figure size ...>"]
                },
                "metadata": {}
            })
            
        print(f"Cell {cell_idx+1} executed successfully. Generated {len(captured_figs)} plot(s).")
    except Exception as e:
        print(f"Error in cell {cell_idx+1}: {e}")
        import traceback
        traceback.print_exc()
        cell['outputs'].append({
            "output_type": "error",
            "ename": type(e).__name__,
            "evalue": str(e),
            "traceback": [str(e)]
        })
    finally:
        sys.stdout = old_stdout
        plt.show = old_show

# Save back pre-rendered notebook
with open('dan_so_visualization.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Pre-rendered notebook saved with all embedded images and outputs!")
