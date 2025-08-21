from . import (
    classify_video_zero_shot,
    cluster_embeddings,
    detect_lewd_images,
    detect_text_in_image_tesseract,
    dimension_reduction,
    image_vec_rep_resnet,
    vid_vec_rep_clip,
    video_hash_tmk,
)

all_operators = [
    classify_video_zero_shot,
    cluster_embeddings,
    detect_lewd_images,
    detect_text_in_image_tesseract,
    dimension_reduction,
    image_vec_rep_resnet,
    vid_vec_rep_clip,
    video_hash_tmk,
]
