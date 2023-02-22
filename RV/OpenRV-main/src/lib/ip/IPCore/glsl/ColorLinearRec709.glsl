//
// Copyright (C) 2023  Autodesk, Inc. All Rights Reserved. 
// 
// SPDX-License-Identifier: Apache-2.0 
//
//
//  Convert from linear to Rec709 
//
//  NOTE: this code is manually vectorized.
//

vec4 ColorLinearRec709 (const in vec4 P)
{
    const vec3 q = vec3(0.018);
    const vec3 a = vec3(0.099);
    const vec3 b = vec3(4.5);
    const vec3 g = vec3(0.45);

    vec3  c = max(P.rgb, vec3(0.0));
    bvec3 t = lessThanEqual(c, q);
    vec3 c0 = c * b;
    vec3 c1 = (vec3(1.0) + a) * pow(c, g) - a;
    return vec4(mix(c1, c0, vec3(t)), P.a);
}
