def semFinishUp(stubs, destFlag='destdir', ext='.java'):
    if getFlag('nowrite'):
        return
    global STD
    dst = getFlag(destFlag)
    if not dst:
        death('illegal destdir flag value')
    try:
        os.mkdir(str(dst))
        debug('[semFinishUp] ' + dst + ': destination subdirectory created')
    except FileExistsError:
        debug('[semFinishUp] ' + dst + ': destination subdirectory exists')
    except:
        death(dst + ': error creating destination subdirectory')
    print('\n{} source files created:'.format(dst))
    # print *all* of the generated files
    for cls in sorted(stubs):
        if cls in STD:
            death('{}: reserved class name'.format(cls))
        try:
            fname = '{}/{}{}'.format(dst, cls, ext)
            with open(fname, 'w') as f:
                print(stubs[cls], end='', file=f)
        except:
            death('cannot write to file {}'.format(fname))
        print('  {}{}'.format(cls, ext))

