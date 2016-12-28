#!/usr/bin/env bash
for BINARY in $(find . -type f | grep '\.dylib$'); do
    for LINK_DESTINATION in $(otool -L ${BINARY} | grep -v : | cut -f1 -d' ' | grep '^\tlib'); do
        BINARY_BASE=$(basename ${BINARY})
        LINK_BASE=$(basename ${LINK_DESTINATION})

        if [[ ${BINARY_BASE} == ${LINK_BASE} ]]; then
            install_name_tool -id "@executable_path/${LINK_BASE}" "$BINARY"
        else
            install_name_tool -change "${LINK_DESTINATION}" "@executable_path/${LINK_BASE}" "${BINARY}"
        fi
    done
done
