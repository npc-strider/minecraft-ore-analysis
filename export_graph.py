from graph import main
import mpld3
import matplotlib.pyplot as plt
from pathlib import Path

output_path = Path('RESULTS')
output_path.mkdir(exist_ok=True)

plot = main(style='default',
            show_bounds=False,
            linewidth=2,
            dpi=100,
            size=[16,10])
mpld3.save_html(plot[1][0], str(output_path / Path('abs_freq.html')), template_type='simple')
mpld3.save_html(plot[1][1], str(output_path / Path('rel_freq.html')), template_type='simple')
plt.close("all")

plot = main(style='dark_background',
            show_bounds=True,
            linewidth=0.75,
            dpi=100,
            size=[16,10])
plot[1][0].savefig(str(output_path / Path('abs_freq.png')))
plot[1][1].savefig(str(output_path / Path('rel_freq.png')))
plot[0].show()
