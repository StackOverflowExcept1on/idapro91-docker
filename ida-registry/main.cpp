#include <cstdio>
#include <cstdlib>
#include <dlfcn.h>

template<class T>
class qvector {
public:
    T *array;
    size_t n, alloc;
};

template<class qchar>
class _qstring {
public:
    qvector<qchar> body;
};

typedef _qstring<const char> qstring; //here we use `const char` but not just `char` (because `str.body.array` is refers to `const char *`)
typedef qvector<qstring> qstrvec_t;

void reg_write_strlist(const qstrvec_t &in, const char *subkey);
void reg_str_set(const char *name, const char *subkey, const char *buf);
int reg_int_op(const char *name, bool save, int value, const char *subkey);

int main() {
    auto handle = dlopen("./libida.so", RTLD_LAZY);

    if (!handle) {
        fprintf(stderr, "%s\n", dlerror());
        return EXIT_FAILURE;
    }

    dlerror();

    auto reg_write_strlist_fptr = reinterpret_cast<decltype(&reg_write_strlist)>(dlsym(handle, "reg_write_strlist"));
    auto reg_str_set_fptr = reinterpret_cast<decltype(&reg_str_set)>(dlsym(handle, "reg_str_set"));
    auto reg_int_op_fptr = reinterpret_cast<decltype(&reg_int_op)>(dlsym(handle, "reg_int_op"));

    qstring str;
    str.body.array = "{\"licsrc\":{\"path\":\"/opt/ida-pro-9.1/idapro.hexlic\"},\"lid\":\"48-2137-ACAB-99\"}\0";
    str.body.n = 77;
    str.body.alloc = 77;

    qstrvec_t vec;
    vec.array = &str;
    vec.n = 1;
    vec.alloc = 1;

    reg_write_strlist_fptr(vec, "Licenses\\IDAPRO.ida-pro");

    reg_str_set_fptr("Python3TargetDLL", nullptr, "/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0");
    reg_int_op_fptr("Use90ShortcutSet", true, 1, nullptr);
    reg_int_op_fptr("EULA 90", true, 1, nullptr);
    reg_int_op_fptr("LicensePrevWarnTime", true, 0, nullptr);
    reg_int_op_fptr("AutoCheckUpdates", true, 0, nullptr);
    reg_int_op_fptr("AutoUseLumina", true, 0, nullptr);
    reg_int_op_fptr("InformedAboutUpdates3", true, 1, nullptr);

    return EXIT_SUCCESS;
}
