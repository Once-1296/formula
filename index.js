const BACKGROUND = "#101010"
const FOREGROUND = "#fc2313ff"
const BORDER = 'rgba(135, 206, 235, 0.2)'

console.log(game)
game.width = Math.min(window.innerWidth,window.innerHeight)
game.height = game.width
const ctx = game.getContext("2d")
console.log(ctx)

function clear() {
    ctx.fillStyle = BACKGROUND
    ctx.fillRect(0, 0, game.width, game.height)
}

function point({x, y}) {
    const s = 20;
    ctx.fillStyle = FOREGROUND
    ctx.fillRect(x - s/2, y - s/2, s, s)
}

function line(p1, p2) {
    ctx.lineWidth = 3;
    ctx.strokeStyle = FOREGROUND
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
}

function line_border(p1, p2) {
    ctx.lineWidth = 3;
    ctx.strokeStyle = BORDER
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
}

function screen(p) {
    // -1..1 => 0..2 => 0..1 => 0..w
    return {
        x: (p.x + 1)/2*game.width,
        y: (1 - (p.y + 1)/2)*game.height,
    }
}

function project({x, y, z}) {
    return {
        x: x/z,
        y: y/z,
    }
}

const FPS = 60;


function translate_z({x, y, z}, dz) {
    return {x, y, z: z + dz};
}

function rotate_xz({x, y, z}, angle) {
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    return {
        x: x*c-z*s,
        y,
        z: x*s+z*c,
    };
}

function rotate_yz({x, y, z}, angle) {
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    return {
        x: x,
        y: y*c-z*s,
        z: y*s+z*c,
    };
}

function rotate_arbitrary({x,y,z},{nx,ny,nz},angle){
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    return {
        // Rodrigues Rotation formula
        x: x*(c+(1-c)*nx*nx) + y*((1-c)*nx*ny-nz*s) + z*((1-c)*nx*nz+ny*s),
        y: x*((1-c)*nx*ny+nz*s) + y*(c+(1-c)*ny*ny) + z*((1-c)*ny*nz-nx*s),
        z: x*((1-c)*nx*nz-ny*s) + y*((1-c)*ny*nz+nx*s) + z*(c+(1-c)*nz*nz),
    };
}

let dz = 1;
let angle = 0;

function frame() {
    const dt = 1/FPS;
    // dz += 1*dt;
    angle += Math.PI*dt;
    clear()
    // for (const v of vs) {
    //     point(screen(project(translate_z(rotate_xz(v, angle), dz))))
    // }
    for (const f of fs) {
        // console.log(f)
        for (let i = 0; i < f.length; ++i) {
            const a = vs[f[i]];
            const b = vs[f[(i+1)%f.length]];
            line(screen(project(translate_z(rotate_arbitrary(a,{nx:0,ny:1,nz:0}, angle), dz))),
                 screen(project(translate_z(rotate_arbitrary(b,{nx:0,ny:1,nz:0}, angle), dz))))
            // line(screen(project(translate_z(rotate_arbitrary(a,{nx:1/Math.sqrt(2),ny:1/Math.sqrt(2),nz:0}, angle), dz))),
            //      screen(project(translate_z(rotate_arbitrary(b,{nx:1/Math.sqrt(2),ny:1/Math.sqrt(2),nz:0}, angle), dz))))
        }
    }
    // for (const f of fs2) {
    //     for (let i = 0; i < f.length; ++i) {
    //         const a = vs[f[i]];
    //         const b = vs[f[(i+1)%f.length]];
    //         line_border(screen(project(translate_z(rotate_arbitrary(a,{nx:0,ny:1,nz:0}, angle), dz))),
    //              screen(project(translate_z(rotate_arbitrary(b,{nx:0,ny:1,nz:0}, angle), dz))))
    //     }
    // }
    setTimeout(frame, 2000/FPS);
}
setTimeout(frame, 2000/FPS);
