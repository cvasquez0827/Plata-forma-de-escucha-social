# Plataforma de IA de Escucha Social

## Resumen ejecutivo

Este repositorio contiene tanto el **PRD completo** como un **primer prototipo funcional** para ejecutar analítica básica de escucha social. El objetivo es ofrecer una base extensible que permita:

- Ingerir publicaciones desde múltiples fuentes (actualmente JSON local de ejemplo, fácilmente extensible a APIs públicas).
- Ejecutar heurísticas de sentimiento y clasificación temática orientadas a Latinoamérica.
- Generar agregaciones rápidas (distribución de sentimiento, volumen por país, línea de tiempo) que alimenten tableros o integraciones.

## Instalación y uso rápido

1. Cree un entorno virtual con Python ≥ 3.11.
2. Instale el paquete en modo editable:

   ```bash
   pip install -e .
   ```

3. Ejecute el pipeline con la configuración de muestra incluida:

   ```bash
   social-listening config.sample.json
   ```

   El comando imprimirá en consola los insights agregados y las publicaciones enriquecidas.

4. Para guardar los resultados en disco, añada `--output insights.json`.

### Extender la ingesta

Los conectores se registran en `social_listening.pipeline.SOURCE_REGISTRY`. Para sumar un nuevo origen (por ejemplo, una API de Twitter mediante snscrape o un crawler de foros), cree una clase que herede de `SocialSource` y agréguela al registro.

### Clasificación temática

Las palabras clave por tópico se definen en el archivo de configuración JSON (`config.sample.json`). Edite la sección `topics.keywords` para mapear términos locales de cada país/industria.

### Pruebas

El módulo de sentimiento cuenta con pruebas unitarias de referencia:

```bash
pytest
```

---

## PRD / SRS – Contexto LATAM

- **Versión:** 1.0  
- **Solicitante / Product Owner:** Cristian Vasquez  
- **Objetivo general:** Construir un software de IA más robusto que herramientas tipo DINAMIC, enfocado en análisis de conversaciones públicas en redes y medios, con contexto social, geográfico y discursivo para Latinoamérica, y con APIs que permitan integrar resultados en BI/ERP/WMS u otros tableros internos.

---

## 1. Problema y oportunidad

Las soluciones de social listening convencionales describen volumen y sentimiento, pero:

- Carecen de contexto sociocultural (modismos, ironías, códigos locales por país o ciudad).
- Ofrecen explicabilidad limitada (por qué el modelo concluye X o Y).
- No integran fuertemente geolocalización y metadatos demográficos estimados.
- Poseen cobertura desigual en LATAM y manejo pobre de ruido o bots.
- Dificultan la integración operativa (APIs poco claras, exportaciones restringidas).

**Oportunidad:** Unificar captura multi-fuente y NLP/LLM con taxonomías locales, detección de actores (personas, marcas, medios, bots), trazabilidad de evidencias y API first para servir tanto a marketing/comunicación como a operaciones (e-commerce/logística/servicio al cliente).

---

## 2. Alcance (Scope)

### 2.1 Fuentes (ingesta)

- **Redes sociales:** X/Twitter, Facebook (páginas públicas y comentarios), Instagram (público), YouTube (títulos, descripciones, comentarios), TikTok (público cuando sea posible), Reddit, foros locales.
- **Medios digitales:** RSS, sites de noticias, blogs.
- **Marketplaces y reseñas:** Amazon, Mercado Libre, Play Store, App Store (según TOS/viabilidad).
- **Gobierno/entidades:** Comunicados públicos.
- **Fuentes internas opcionales:** Tickets, NPS, chat del e-commerce (si el cliente provee y consiente).

> **Nota legal:** Solo contenidos públicos y en cumplimiento de TOS/leyes (ver sección 10).

### 2.2 Idiomas y países

- Español LATAM (países principales), portugués Brasil, inglés básico para préstamos/regionalismos.
- **Países prioritarios:** Perú, México, Chile, Colombia, Argentina, Brasil.

### 2.3 Usuarios objetivos

- Analistas de reputación/marketing.
- Comunicación corporativa y asuntos públicos.
- Equipos de operaciones que quieran disparar alertas por temas logísticos o de servicio.

---

## 3. Funcionalidades clave

### 3.1 Ingesta y normalización

- Conectores con rate limit aware, backoff y colas.
- De-duplicación, canonicalización de URLs, enriquecimiento de metadatos (fuente, autor, timestamp, enlace).
- Detección de idioma y variantes locales.
- Parser de emojis, hashtags, menciones (@), links (expand link preview si es posible).

### 3.2 Enriquecimiento y análisis (NLP/LLM)

- Clasificación temática (taxonomía configurable por industria o país).
- Detección de entidades (personas, marcas, productos, lugares, instituciones, políticos).
- Geolocalización: por metadatos, por texto (topónimo) y por señales indirectas (inferidas).
- Sentimiento (positivo/negativo/neutral) y actitud/stance (a favor/en contra/neutral de una entidad o propuesta).
- Detección de ironía o sarcasmo y modismos locales mediante adaptación por país (fine-tuning o prompt + RAG con glosarios).
- Topic modeling (LDA/BERTopic) y clustering por conversación o tendencia.
- Detección de bots/trolls y spam (comportamiento, red de retuits, repetición, boosting anómalo).
- Resumen explicativo con trazabilidad: el insight siempre enlaza a ejemplos concretos.
- Eventos: picos, quiebres de tendencia, narrativas emergentes.
- Comparativos: por país, segmento, canal y período.

### 3.3 Panel e insights

- Dashboard con KPI: volumen, alcance estimado, sentimiento, share of voice, entidades top, tópicos, mapas, evolución temporal.
- Explorador de hilos/conversaciones con filtros: país, ciudad, fuente, entidad, tema, sentimiento, stance, periodo.
- Alertas: reglas (si [métrica] > umbral) y alertas inteligentes (detección de anomalías).
- Reportes exportables (PDF, PPTX, CSV/Parquet) con plantillas editables.

### 3.4 API / Integraciones (API-first)

- REST + Webhooks (y opción GraphQL).
- SDKs: Python y JavaScript.
- Conectores: Power BI, BigQuery, Snowflake; Webhook para ERP/WMS/CRM.
- Streaming: endpoint para eventos en tiempo casi real.
- Autenticación: OAuth2/JWT, claves por proyecto.

### 3.5 Admin / Gobernanza de datos

- Proyectos o espacios por cliente y país.
- Roles y permisos (RBAC): admin, analista, lector, integraciones.
- Data lineage: desde el post original hasta el insight.
- Retención configurable y pseudonimización de identificadores cuando aplique.

---

## 4. Requisitos no funcionales

- Escalabilidad: 50–200M de documentos/mes (escalado horizontal en ingesta y NLP).
- Latencia objetivo: menos de 5 minutos de backlog para posts nuevos en canales prioritarios.
- Disponibilidad: ≥ 99.5 % mensual.
- Costos: arquitectura cloud-cost aware con colas, lotes, caché de resultados y modelos compactos cuando sea viable.
- Observabilidad: logs estructurados, métricas (Prometheus/OpenTelemetry), trazas.

---

## 5. Arquitectura propuesta (alto nivel)

- **Ingesta** (microservicios): conectores por fuente + Kafka/PubSub; almacenamiento crudo en data lake (object storage).
- **Procesamiento**:
  - Batch + streaming (Spark/Flink/Beam o similar).
  - **Servicio NLP/LLM**:
    - Modelos base (mBERT/XLM-R + LLMs) con adapters (LoRA/PEFT) por país.
    - RAG con glosarios locales y listas de entidades (catálogos).
    - Micro-servicio de stance y sarcasmo.
    - Servicio de detección de bots (características de red + heurísticas + GNN opcional).
- **Almacenamiento procesado**: data warehouse (BigQuery/Snowflake) + Elastic/Opensearch para búsqueda rápida.
- **APIs**: Gateway (REST/GraphQL), autenticación, rate limiting.
- **UI**: SPA (React/Vue) + mapas (Mapbox/Leaflet), gráficos (ECharts/Recharts).
- **MLOps**: DVC/Weights & Biases/MLflow; CI/CD con tests y canary de modelos.

---

## 6. Modelado y entrenamiento

- Conjuntos de entrenamiento específicos por país y vertical (annotators nativos).
- Etiquetas: sentimiento, stance vs entidad, tema, sarcasmo, toxicidad, bot/spam.
- Human-in-the-loop: corrección de etiquetas desde el panel; active learning.
- Evaluación (mínimos por versión):
  - Sentimiento macro-F1 ≥ 0.80 (es-LATAM).
  - Stance macro-F1 ≥ 0.75 en 3+ países.
  - Sarcasmo F1 ≥ 0.60 (objetivo inicial) con mejora continua.
  - Bot-detection AUC ≥ 0.85.
  - Geoparsing precisión ciudad/país ≥ 0.85 (cuando hay evidencia textual).
- Mitigación de sesgos: evaluación por país/segmento; reportes de fairness.
- Explicabilidad: SHAP/LIME para clasificadores tradicionales, rationales para LLMs.

---

## 7. Esquemas de datos (simplificados)

### 7.1 Objeto `Post` (normalizado)

```json
{
  "post_id": "string",
  "source": "twitter|facebook|youtube|...",
  "url": "string",
  "author_id": "string",
  "author_meta": {"verified": false, "followers": 0, "lang": "es"},
  "timestamp": "ISO8601",
  "text": "string",
  "media": [{"type": "image|video", "url": "string"}],
  "lang": "es-PE",
  "country": "PER",
  "city": "Lima",
  "geo_confidence": 0.78,
  "entities": [{"type": "PERSON|ORG|PRODUCT|LOC", "text": "...", "qid": "optional"}],
  "topics": ["entregas", "precios"],
  "sentiment": {"label": "pos|neg|neu", "score": 0.91},
  "stance": [{"target": "MarcaX", "label": "pro|contra|neu", "score": 0.74}],
  "sarcasm": {"is_sarcastic": false, "score": 0.11},
  "toxicity": {"label": "safe|toxic", "score": 0.08},
  "bot_score": 0.13,
  "thread_id": "string",
  "parent_id": "string|null"
}
```

### 7.2 Objeto `Insight`

```json
{
  "insight_id": "string",
  "project_id": "string",
  "title": "Reclamos por demora en Lima aumentaron 35%",
  "period": {"from": "2025-10-01", "to": "2025-10-31"},
  "evidence": ["post_id_1", "post_id_9", "post_id_33"],
  "metrics": {"delta_volume": 0.35, "sentiment_shift": -0.12},
  "segments": {"city": "Lima", "source": "twitter"},
  "explanation": "Aumento coincide con quiebre de stock en tiendas centro.",
  "links": ["/dash/insights/abc"]
}
```

---

## 8. API (borrador)

### 8.1 Autenticación

- `POST /auth/token` → JWT (scopes por proyecto).

### 8.2 Ingesta

- `POST /v1/sources/webhook` (opcional) – recepción de eventos.

### 8.3 Consulta

- `GET /v1/posts?query=...&country=PER&from=2025-10-01&to=2025-10-31&entity=MarcaX&sentiment=neg`
- `GET /v1/insights?project_id=...&from=...&to=...`
- `GET /v1/trends/topics?country=PER&granularity=day`
- `GET /v1/entities/top?country=PE&limit=50`

### 8.4 Exportación

- `POST /v1/exports` → genera CSV/Parquet + URL temporal (S3/GCS signed URL).

### 8.5 Alertas

- `POST /v1/alerts` (reglas), `GET /v1/alerts/:id`, webhooks de disparo.

---

## 9. Seguridad, privacidad y cumplimiento

- Cumplir TOS de cada plataforma; solo contenido público.
- PII mínimo: no almacenar datos sensibles innecesarios; hash/pseudónimo de `author_id` cuando aplique.
- Consentimiento y DPA cuando se usen fuentes internas del cliente.
- Retención por proyecto (p. ej., 12–24 meses configurable).
- Cifrado en tránsito (TLS 1.2+) y en reposo (KMS).
- Auditoría de accesos; RBAC; registros de descarga/exportación.
- Política de eliminación (right-to-erasure sobre datos propios cuando aplique legalmente).
- Ethics by design: documentación de límites, disclaimers de inferencias.

---

## 10. UX/UI (borrador)

- Home dashboard: KPI claves, cards de alertas, mapa de calor, nubes de tópicos/entidades.
- Explorer: tabla y vista de hilo, filtros persistentes, panel derecho con explicación del modelo y evidencias citables.
- Comparador: países/canales/periodos lado a lado.
- Constructor de reportes: arrastrar-soltar módulos, portada, comentarios, exportación a PPTX/PDF.
- Gestión de taxonomías: editor visual de temas/subtemas por país/industria.
- Etiquetado humano: interfaz para feedback (HITL) y active learning.

---

## 11. Roadmap sugerido

### MVP (8–12 semanas)

1. Ingesta X/Twitter + YouTube + RSS (noticias).
2. Pipeline NLP: idioma, entidades, temas (taxonomía inicial), sentimiento.
3. Dashboard básico + búsquedas + exportación CSV.
4. API consulta + autenticación.
5. Alertas por umbral + correo/webhook.
6. Bot-detection v0 (heurística + reglas).
7. País piloto (Perú) con glosario local.

### V2

- Stance, sarcasmo, geoparsing avanzado, comparador multi-país, reportes PPTX, conectores BI, modelos adaptados por país, bot-detection ML completo.

### V3

- Streaming a gran escala, GraphQL, explicabilidad avanzada, fairness dashboards, GNN para redes de propagación, conectores marketplaces/reviews.

---

## 12. Métricas de éxito (OKR/KPI)

- Cobertura: % de fuentes configuradas vs planificadas; posts/mes indexados.
- Calidad NLP: F1 por tarea/país; intervalos de confianza visibles.
- Latencia: p95 de ingesta a insight.
- Uso: MAU, consultas/día, exportaciones, alertas resueltas.
- Impacto: casos con decisión accionable (p. ej., ajuste logístico) documentados.

---

## 13. Criterios de aceptación (extracto)

- El sistema indexa ≥ 3 fuentes (X, YouTube, RSS) y procesa ≥ 1M posts en el piloto.
- Búsqueda por entidad + país + fecha responde en < 2 s (p95) sobre 30 días.
- Sentimiento macro-F1 ≥ 0.80 (es-PE) con reporte de validación.
- Exportación CSV con todos los campos definidos en `Post`.
- Alertas configurables con webhook funcional (entrega confirmada).
- Panel con trazabilidad (al menos 3 evidencias por insight).
- RBAC: admin crea proyectos y gestiona permisos por rol.

---

## 14. Anexos

### 14.1 Glosarios y taxonomías (borrador)

- **Retail/Logística:** entrega, stock, precio, cambio, garantía, tienda, sede, courier, demora, embalaje, devolución, reposición, atención, call center.
- **Política/Público:** economía, seguridad, corrupción, elecciones, transporte, salud, educación, protestas, propuestas, encuestas.
- **Sentimiento/stance:** pro/contra/neutro; intensidad (0–1).

### 14.2 Riesgos

- Cambios en TOS/API de redes; cobertura desigual por país; costo de GPU/LLM; calidad de anotación; sesgos regionales.

---

## 15. Entregables para CODEX

- **Infra:** IaC (Terraform) + diagramas de arquitectura.
- **Código:** repos microservicios (ingesta, NLP, API, UI), pruebas, Dockerfiles.
- **Datasets:** muestras etiquetadas por país; guía de anotación.
- **MLOps:** pipelines de entrenamiento/evaluación, versionado de modelos.
- **Manual de API:** OpenAPI/Swagger y playground.
- **Guía de despliegue:** dev/stg/prod + control de costos.

---

## 16. Extras opcionales para Cristian

- Webhook que empuje picos de “quejas de entrega” a ERP/WMS para abrir un ticket o disparar una revisión de rutas/stock.
- Plantilla de PPTX autogenerada para comité semanal (3 slides por marca/país).
- Exportación a BigQuery para cruzar con ventas/stock.

