export interface User {
    id: bigint
    username: string
    email: string
    date_verified_email: string | null
    avatar: string | null
    first_name: string | null
    last_name: string | null
    date_joined: string
    followers?: Follower[]
    following?: Following[]
}

export interface Follower {
    follower: User
    date_created: string
}

export interface Following {
    following: User
    date_created: string
}
