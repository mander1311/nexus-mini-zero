document.addEventListener("DOMContentLoaded", () => {
  const navItems = document.querySelectorAll(".nav-item");
  const panels = document.querySelectorAll(".panel");

  navItems.forEach((button) => {
    button.addEventListener("click", () => {
      navItems.forEach((item) => item.classList.toggle("active", item === button));
      panels.forEach((panel) => {
        panel.classList.toggle("active-panel", panel.id === button.dataset.section);
      });
    });
  });

  const form = document.getElementById("product-form");
  const tableBody = document.getElementById("products-table");
  const analysisList = document.getElementById("analysis-list");
  const refreshButton = document.getElementById("refresh-data");
  const resetFormButton = document.getElementById("reset-form");

  const metricTotal = document.getElementById("metric-total");
  const metricOpportunities = document.getElementById("metric-opportunities");
  const metricSelected = document.getElementById("metric-selected");
  const metricCommission = document.getElementById("metric-commission");

  const fields = {
    id: document.getElementById("product-id"),
    name: document.getElementById("product-name"),
    marketplace: document.getElementById("product-marketplace"),
    category: document.getElementById("product-category"),
    price: document.getElementById("product-price"),
    rate: document.getElementById("product-rate"),
    rating: document.getElementById("product-rating"),
    reviews: document.getElementById("product-reviews"),
    demand: document.getElementById("product-demand"),
    competition: document.getElementById("product-competition"),
    link: document.getElementById("product-link"),
    affiliate: document.getElementById("product-affiliate"),
    notes: document.getElementById("product-notes"),
  };

  function formatMoney(value) {
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(value || 0));
  }

  async function fetchJSON(url, options = {}) {
    const response = await fetch(url, { headers: { "Content-Type": "application/json" }, ...options });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "Erro ao processar requisição.");
    }
    return response.json();
  }

  async function loadDashboard() {
    const data = await fetchJSON("/api/dashboard");
    metricTotal.textContent = data.total_products;
    metricOpportunities.textContent = data.opportunities;
    metricSelected.textContent = data.selected_products;
    metricCommission.textContent = formatMoney(data.potential_commission);
  }

  function renderProducts(products) {
    tableBody.innerHTML = "";
    products.forEach((product) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>
          <strong>${product.name}</strong><br>
          <small>${product.category || "Geral"}</small>
        </td>
        <td>${product.marketplace || "Manual"}</td>
        <td>${formatMoney(product.price)}</td>
        <td>${formatMoney(product.commission_estimate)} (${Number(product.commission_rate || 0).toFixed(2)}%)</td>
        <td>${(product.score || 0).toFixed(1)}</td>
        <td>${product.favorite ? "★" : "☆"}</td>
        <td>
          <button class="action-btn" data-action="edit" data-id="${product.id}">Editar</button>
          <button class="action-btn" data-action="favorite" data-id="${product.id}">${product.favorite ? "Desfavoritar" : "Favoritar"}</button>
          <button class="action-btn danger" data-action="delete" data-id="${product.id}">Excluir</button>
        </td>
      `;
      tableBody.appendChild(row);
    });

    tableBody.querySelectorAll(".action-btn").forEach((button) => {
      button.addEventListener("click", async () => {
        const { action, id } = button.dataset;
        const product = products.find((item) => String(item.id) === id);
        if (!product) return;

        if (action === "edit") {
          populateForm(product);
          document.querySelector('[data-section="products"]').click();
        }

        if (action === "favorite") {
          await fetchJSON(`/api/products/${id}`, {
            method: "PUT",
            body: JSON.stringify({ favorite: !product.favorite }),
          });
          await loadProducts();
        }

        if (action === "delete") {
          await fetchJSON(`/api/products/${id}`, { method: "DELETE" });
          await loadProducts();
        }
      });
    });
  }

  function populateForm(product) {
    fields.id.value = product.id;
    fields.name.value = product.name || "";
    fields.marketplace.value = product.marketplace || "Manual";
    fields.category.value = product.category || "";
    fields.price.value = product.price || 0;
    fields.rate.value = product.commission_rate || 0;
    fields.rating.value = product.rating || 0;
    fields.reviews.value = product.review_count || 0;
    fields.demand.value = product.search_interest || 0;
    fields.competition.value = product.competition || 0;
    fields.link.value = product.product_link || "";
    fields.affiliate.value = product.affiliate_link || "";
    fields.notes.value = product.notes || "";
  }

  async function loadProducts() {
    const products = await fetchJSON("/api/products");
    const productsWithScore = await Promise.all(products.map(async (product) => {
      try {
        const data = await fetchJSON(`/api/products/${product.id}/analysis`);
        return { ...product, score: data.score || 0 };
      } catch {
        return { ...product, score: 0 };
      }
    }));
    renderProducts(productsWithScore);
    renderAnalysis(productsWithScore);
    await loadDashboard();
  }

  function renderAnalysis(products) {
    analysisList.innerHTML = "";
    const topProducts = [...products].sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 5);
    if (!topProducts.length) {
      analysisList.innerHTML = "<div class='analysis-item'><h4>Sem dados</h4><p>Cadastre produtos para ver a análise.</p></div>";
      return;
    }

    topProducts.forEach((product) => {
      const item = document.createElement("div");
      item.className = "analysis-item";
      item.innerHTML = `
        <h4>${product.name}</h4>
        <p>Marketplace: ${product.marketplace || "Manual"}</p>
        <p>Score balanced: <strong>${Number(product.score || 0).toFixed(2)}</strong></p>
        <p>Comissão estimada: ${formatMoney(product.commission_estimate)}</p>
      `;
      analysisList.appendChild(item);
    });
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      name: fields.name.value,
      marketplace: fields.marketplace.value,
      category: fields.category.value,
      price: Number(fields.price.value || 0),
      commission_rate: Number(fields.rate.value || 0),
      rating: Number(fields.rating.value || 0),
      review_count: Number(fields.reviews.value || 0),
      search_interest: Number(fields.demand.value || 0),
      competition: Number(fields.competition.value || 0),
      product_link: fields.link.value,
      affiliate_link: fields.affiliate.value,
      notes: fields.notes.value,
      favorite: false,
      selected: false,
    };

    const id = fields.id.value;
    if (id) {
      await fetchJSON(`/api/products/${id}`, { method: "PUT", body: JSON.stringify(payload) });
    } else {
      await fetchJSON("/api/products", { method: "POST", body: JSON.stringify(payload) });
    }

    form.reset();
    resetForm();
    await loadProducts();
  });

  function resetForm() {
    form.reset();
    fields.marketplace.value = "Amazon";
    fields.price.value = 0;
    fields.rate.value = 0;
    fields.rating.value = 0;
    fields.reviews.value = 0;
    fields.demand.value = 0;
    fields.competition.value = 0;
    fields.id.value = "";
  }

  resetFormButton.addEventListener("click", resetForm);
  refreshButton.addEventListener("click", loadProducts);

  document.getElementById("calculate-btn").addEventListener("click", async () => {
    const payload = {
      price: Number(document.getElementById("calc-price").value || 0),
      commission_rate: Number(document.getElementById("calc-rate").value || 0),
      sales: Number(document.getElementById("calc-sales").value || 1),
      conversion_rate: Number(document.getElementById("calc-conversion").value || 0) / 100,
    };
    const result = await fetchJSON("/api/calculator", { method: "POST", body: JSON.stringify(payload) });
    document.getElementById("calculator-output").textContent = JSON.stringify(result, null, 2);
  });

  document.getElementById("copy-btn").addEventListener("click", async () => {
    const payload = {
      name: document.getElementById("copy-name").value || "Produto",
      marketplace: document.getElementById("copy-marketplace").value || "Amazon",
      price: Number(document.getElementById("copy-price").value || 0),
      commission_rate: Number(document.getElementById("copy-rate").value || 0),
    };
    const result = await fetchJSON("/api/copywriter", { method: "POST", body: JSON.stringify(payload) });
    document.getElementById("copy-output").textContent = JSON.stringify(result, null, 2);
  });

  resetForm();
  loadProducts();
});
