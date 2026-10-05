#!/bin/bash
# render.sh — reconstruye, valida, exporta a PDF y arma las hojas de contacto para la revisión visual
set -e
cd "$(dirname "$0")"
node gen.js
python3 /mnt/skills/public/pptx/scripts/office/validate.py Tesina_MTI_IA_Aplicada.pptx
pkill -9 -f soffice || true
sleep 1
P=/tmp/lo-$(date +%s)
mkdir -p "$P"
rm -f Tesina_MTI_IA_Aplicada.pdf slide-*.jpg qa-*.jpg
timeout 400 soffice --headless --norestore -env:UserInstallation=file://$P \
  --convert-to pdf --outdir . Tesina_MTI_IA_Aplicada.pptx >/dev/null 2>&1 || true
[ -f Tesina_MTI_IA_Aplicada.pdf ] || { echo "FALLO: no se generó el PDF"; exit 1; }
pdftoppm -jpeg -r 100 Tesina_MTI_IA_Aplicada.pdf slide
python3 - <<'PY'
from PIL import Image
import glob
fs = sorted(glob.glob('slide-*.jpg'))
for k in range(0, len(fs), 6):
    g = fs[k:k+6]; ims = [Image.open(f) for f in g]; w, h = ims[0].size
    sheet = Image.new('RGB', (w*2, h*3), 'white')
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2)*w, (i//2)*h))
    sheet.save('qa-%02d.jpg' % (k//6+1), quality=88)
print('laminas:', len(fs))
PY
