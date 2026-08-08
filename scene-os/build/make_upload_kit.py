#!/usr/bin/env python3
"""Copy pipeline outputs into skool-upload/ under student-facing names."""
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'skool-upload')

MAP = {
 'pdfs/00_The-SCENE-AI_Start-Here_Production-Blueprint.pdf': 'The Production Blueprint.pdf',
 'pdfs/01_The-SCENE-AI_Module-01_Character-First.pdf': 'Module 01 - Character First.pdf',
 'pdfs/02_The-SCENE-AI_Module-02_The-Prompt-Pack.pdf': 'Module 02 - The Prompt Pack.pdf',
 'pdfs/03_The-SCENE-AI_Module-03_The-SCENE-Method.pdf': 'Module 03 - The SCENE Method.pdf',
 'pdfs/04_The-SCENE-AI_Module-04_The-SCENE-Library.pdf': 'Module 04 - The SCENE Library.pdf',
 'pdfs/05_The-SCENE-AI_Module-05A_Womens-Outfit-Pack.pdf': 'Module 05A - Her Outfit Pack.pdf',
 'pdfs/06_The-SCENE-AI_Module-05B_Mens-Outfit-Pack.pdf': 'Module 05B - His Outfit Pack.pdf',
 'pdfs/07_The-SCENE-AI_Module-06A_Womens-Hair-Pack.pdf': 'Module 06A - Her Hair Pack.pdf',
 'pdfs/08_The-SCENE-AI_Module-06B_Mens-Hair-Grooming-Pack.pdf': 'Module 06B - His Hair and Grooming.pdf',
 'pdfs/09_The-SCENE-AI_Module-07_The-Reference-Blueprint.pdf': 'Module 07 - The Reference Blueprint.pdf',
 'pdfs/10_The-SCENE-AI_Module-08_The-Continuity-System.pdf': 'Module 08 - The Continuity System.pdf',
 'pdfs/11_The-SCENE-AI_Module-09_Camera-Bible.pdf': 'Module 09 - The Camera Bible.pdf',
 'pdfs/12_The-SCENE-AI_Module-10_Realism-Check.pdf': 'Module 10 - The Realism Check.pdf',
 'pdfs/13_The-SCENE-AI_Module-11_The-Prompt-Vault.pdf': 'Module 11 - The Prompt Vault.pdf',
 'pdfs/14_The-SCENE-AI_Module-12_The-Viral-Story-Blueprint.pdf': 'Module 12 - The Viral Story Blueprint.pdf',
 'pdfs/15_The-SCENE-AI_Bonus-01_Hook-Vault.pdf': 'The Hook Vault.pdf',
 'pdfs/16_The-SCENE-AI_Bonus-02_Caption-Vault.pdf': 'The Caption Vault.pdf',
 'pdfs/17_The-SCENE-AI_Bonus-03_Comment-Blueprint.pdf': 'The Comment Blueprint.pdf',
 'pdfs/18_The-SCENE-AI_Bonus-04_The-SCENE-Files.pdf': 'The SCENE Files.pdf',
 'products/The-SCENE-AI_Cast-Your-Lead_Members-Edition.pdf': 'Cast Your Lead.pdf',
 'products/The-Creator-OS-Map.pdf': 'The Creator OS Map.pdf',
 'products/The-SCENE-AI_Identity-Lock-Mini-Pack.pdf': 'The Identity Lock Mini-Pack.pdf',
 'products/THE-SCENE-AI_Drop-001_The-Vacation-Heat-Drop.pdf': 'Drop 001 - The Vacation Heat Drop.pdf',
 'studio/scene-studio.html': 'SCENE Studio.html',
}
os.makedirs(OUT, exist_ok=True)
for src, dst in MAP.items():
    shutil.copy2(os.path.join(ROOT, src), os.path.join(OUT, dst))
    print('->', dst)
