_base_ = "r50_rsb_a3_CE_none_4xb512_fp16.py"

# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=[0.1, 1.0,],
    mix_mode=["mixup", "cutmix",],
    mix_prob=None,  # None for random applying
    head=dict(
        type='ClsMixupHead',
        loss=dict(type='CrossEntropyLoss',  # mixup BCE loss (one-hot encoding)
            use_soft=False, use_sigmoid=True, loss_weight=1.0),
        with_avg_pool=True, multi_label=True, two_hot=False,
        in_channels=2048, num_classes=1000)
)
