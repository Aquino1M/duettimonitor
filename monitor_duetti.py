import time
import json
from playwright.sync_api import sync_playwright

URLS = [
    {"nome": "Other Language Tracks", "url": "https://whop.com/joined/duetti/viral-other-language-tracks-easy-J3RpOMB9UPhoKT/app/"},
    {"nome": "French Tracks", "url": "https://whop.com/joined/duetti/viral-french-tracks-titres-francais-virals-de-l--KcYtY54EvguR0F/app/"},
    {"nome": "English Tracks", "url": "https://whop.com/joined/duetti/viral-english-tracks-easy-94pnwi16R7jttD/app/"},
    {"nome": "Portuguese Tracks", "url": "https://whop.com/joined/duetti/viral-portuguese-tracks-musicas-portuguesas-que--SNKspmb9RMShkS/app/"},
    {"nome": "Spanish Tracks", "url": "https://whop.com/joined/duetti/viral-spanish-tracks-canciones-espanolas-que-se--g9ptcW3PPbrE4Y/app/"}
]

def verificar_musicas():
    print("A iniciar o robô de monitorização (Visível)... Aguarda.")
    resultados = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # HEADLESS=TRUE PARA O GITHUB ACTIONS!
        try:
            context = browser.new_context(storage_state="auth.json")
        except Exception:
            print("Erro: auth.json não encontrado! Por favor faz login primeiro.")
            return

        page = context.new_page()

        for item in URLS:
            nome_aba = item["nome"]
            url = item["url"]
            musicas_detalhadas = []
            
            print(f"\n--- A analisar página: {nome_aba} ---")
            
            try:
                page.goto(url)
                page.wait_for_timeout(8000) 
                
                cards = page.locator("div:has-text('Paid Out')").all()
                
                if len(cards) == 0:
                    for frame in page.frames:
                        cards_in_frame = frame.locator("div:has-text('Paid Out')").all()
                        if len(cards_in_frame) > 0:
                            cards = cards_in_frame
                            break

                print(f"  -> {len(cards)} possíveis cards de campanha detetados.")
                
                for card in cards:
                    texto_card = card.inner_text().strip()
                    linhas = [l.strip() for l in texto_card.split('\n') if l.strip()]
                    
                    if len(linhas) >= 3 and len(linhas) <= 15:
                        musica = "Desconhecida"
                        valor = "Desconhecido"
                        
                        for i, Server_linha in enumerate(linhas):
                            if "1k views" in Server_linha or "$" in Server_linha:
                                valor = Server_linha
                            if "Duetti" in Server_linha and i > 0:
                                musica = lines[i-1] if 'lines' in locals() else linhas[i-1]
                                
                        if musica != "Desconhecida" and not any(m['musica'] == musica for m in musicas_detalhadas):
                            musicas_detalhadas.append({
                                "musica": musica,
                                "valor": valor
                            })
                            print(f"  ✅ {musica} | {valor}")
                            
                status = "✅ Campanhas Encontradas" if len(musicas_detalhadas) > 0 else "❌ Nenhuma campanha"

            except Exception as e:
                print(f"  -> Erro ao ler {nome_aba}: {e}")
                status = "⚠️ Erro na leitura"
                
            # AGORA SALVA O LINK TAMBÉM!
            resultados.append({
                "aba": nome_aba,
                "url": url,
                "status": status,
                "musicas": musicas_detalhadas
            })

        browser.close()
        
    js_content = f"const scrapingData = {json.dumps(resultados, ensure_ascii=False, indent=2)};"
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("\n==========================================")
    print("CONCLUÍDO! O ficheiro data.js foi atualizado.")
    print("==========================================")

if __name__ == "__main__":
    verificar_musicas()
