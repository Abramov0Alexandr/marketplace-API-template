def product_image_upload_path(model, file) -> str:
    return f"product/{model.shop_name}/{file}"
