_base_ = '../../../../base.py'
# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=1,  # float or list
    mix_mode="mixup",  # str or list, choose a mixup mode
    mix_args=dict(
        manifoldmix=dict(layer=(0, 3)),
        resizemix=dict(scope=(0.1, 0.8), use_alpha=True),
        fmix=dict(decay_power=3, size=(224,224), max_soft=0., reformulate=False)
    ),
    backbone=dict(
        # type='ResNeXt',  # normal
        type='ResNeXt_Mix',  # required by 'manifoldmix'
        depth=101,
        groups=32, width_per_group=4,  # 32x4d
        out_indices=(3,),  # no conv-1, x-1: stage-x
        style='pytorch'),
    head=dict(
        type='ClsHead',  # mixup head, normal CE loss
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        with_avg_pool=True, multi_label=False, in_channels=2048, num_classes=1000)
)
# dataset settings
data_source_cfg = dict(type='ImageNet')
# iNat dataset
data_train_list = 'data/meta/iNaturalist2017/train_labeled_full.txt'
data_train_root = 'data/iNaturalist2017/train'
data_test_list = 'data/meta/iNaturalist2017/val_labeled.txt'
data_test_root = 'data/iNaturalist2017/val/'

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=224),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=256),
    dict(type='CenterCrop', size=224),
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]
# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=64,  # V100: 64 x 4gpus = bs256
    workers_per_gpu=8,  # according to total cpus cores, usually 4 workers per 32~128 imgs
    train=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list, root=data_train_root,
            **data_source_cfg),
        pipeline=train_pipeline,
        prefetch=prefetch,
    ),
    val=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_test_list, root=data_test_root, **data_source_cfg),
        pipeline=test_pipeline,
        prefetch=False,
    ))
# additional hooks
custom_hooks = [
    dict(
        type='ValidateHook',
        dataset=data['val'],
        initial=False,
        interval=1,
        imgs_per_gpu=128,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5)))
]
# optimizer
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# lr scheduler
lr_config = dict(policy='CosineAnnealing', min_lr=0)
checkpoint_config = dict(interval=100)

# runtime settings
total_epochs = 100