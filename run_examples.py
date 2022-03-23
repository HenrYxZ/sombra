import sys
# Local Modules
import examples


def main(argv):
    if "flat_sphere" in argv:
        examples.flat_sphere.main()
    elif "flat_shading_scene" in argv:
        examples.flat_shading_scene.main()
    elif "pathtracer" in argv:
        examples.pathtracing.main()
    elif "atmosphere" in argv:
        examples.atmosphere.main()
    elif "render_interactive" in argv:
        examples.render_interactive.main()


if __name__ == '__main__':
    main(sys.argv[1:])
