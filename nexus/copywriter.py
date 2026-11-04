def generate_copy(product):
    name = (product.get("name") or "produto").strip()
    marketplace = product.get("marketplace") or "mercado"
    price = float(product.get("price") or 0)
    commission_rate = float(product.get("commission_rate") or 0)
    affiliate_note = "Aviso: este conteúdo pode conter link de afiliado."

    title = f"{name} merece atenção no {marketplace}"
    description = (
        f"Descubra {name} com foco em valor, praticidade e relevância para quem busca uma opção interessante. "
        f"O preço atual está em R$ {price:.2f} e a comissão estimada é de {commission_rate:.2f}% por venda."
    )
    caption = (
        f"🤍 {name}\n\n"
        f"Preço atual: R$ {price:.2f}\n"
        f"Comissão estimada: {commission_rate:.2f}%\n\n"
        f"Vale a pena conferir! {affiliate_note}"
    )
    cta = f"Clique para conhecer mais sobre {name} e conferir o produto em {marketplace}."
    short_post = f"{name} está na mira. Preço atual de R$ {price:.2f}. Comissão estimada de {commission_rate:.2f}%. Confira o link. {affiliate_note}"
    video_script = (
        f"[Abertura] Hoje vou mostrar {name}.\n"
        f"[Demonstração] Destaco o valor, uso e utilidade do produto.\n"
        f"[Preço] O valor atual está em R$ {price:.2f}.\n"
        f"[Oferta] Comissão estimada de {commission_rate:.2f}%.\n"
        f"[CTA] Clique no link e confira mais detalhes."
    )

    return {
        "title": title,
        "description": description,
        "caption": caption,
        "cta": cta,
        "short_post": short_post,
        "video_script": video_script,
        "affiliate_note": affiliate_note,
    }
