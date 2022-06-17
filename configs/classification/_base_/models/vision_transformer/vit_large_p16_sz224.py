# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=[0.8, 1.0,],
    mix_mode=["mixup", "cutmix",],
    mix_args=dict(),
    backbone=dict(
        type='VisionTransformer',
        arch='large',
        img_size=224, patch_size=16,
        drop_path_rate=0.2,
    ),
    head=dict(
        type='VisionTransformerClsHead',
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.1, num_classes=1000, mode='original', loss_weight=1.0),
        in_channels=1024, num_classes=1000)
)
