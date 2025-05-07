package com.beoks.demo.hibernate.onetoone

import jakarta.persistence.*

@Entity
@Table(name = "profiles")
data class Profile(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = true)
    var bio: String? = null,

    @Column(nullable = true)
    var avatarUrl: String? = null,

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    var user: User
) {
    init {
        user.profile = this
    }
} 
