import config as cfg

if cfg.IN_AWS_LAMBDA:
    import sys
    import runpy
    # sys.path.insert(0, '')
    sys.argv = ['awslambdaric', 'lambda_.lambda_f']
    runpy.run_module('awslambdaric', run_name='__main__') 
else:
    import lambda_
    import asyncio
    asyncio.run(lambda_.main())