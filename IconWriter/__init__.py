import io

import azure.functions as func
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import staticmaps

app = fastapi.FastAPI()
nest_asyncio.apply()

@app.get("/generate_map")
def main() -> StreamingResponse:
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_StamenToner)

    frankfurt = staticmaps.create_latlng(50.110644, 8.682092)
    newyork = staticmaps.create_latlng(40.712728, -74.006015)

    context.add_object(staticmaps.Line([frankfurt, newyork], color=staticmaps.BLUE, width=4))
    context.add_object(staticmaps.Marker(frankfurt, color=staticmaps.GREEN, size=12))
    context.add_object(staticmaps.Marker(newyork, color=staticmaps.RED, size=12))

    # render non-anti-aliased png
    image_pil = context.render_pillow(800, 500)

    img_byte_arr = io.BytesIO()
    image_pil.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return StreamingResponse(img_byte_arr, media_type="image/png")

async def main(
    req: azure.functions.HttpRequest, context: azure.functions.Context
) -> azure.functions.HttpResponse:
    return azure.functions.AsgiMiddleware(app).handle(req, context)